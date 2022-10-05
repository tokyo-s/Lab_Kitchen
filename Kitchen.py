from Cook import Cook
from Order import Order
from config import *
import threading
import logging
import requests
from queue import PriorityQueue
from Apparatus import *
import time

logger = logging.getLogger(__name__)
DINNING_HALL_URL = "http://dinning-hall-container:8001"


def send_order_for_distribution(order):
    logger.warning('Sending food to dining hall')
    order_json = order.__dict__
    del order_json['food_items']
    del order_json['register_order_time']
    requests.post(f'{DINNING_HALL_URL}/distribution', json=order_json)


class Kitchen:
    def __init__(self, nr_cooks=NR_COOKS, nr_ovens=NR_OVENS, nr_stoves=NR_STOVES):
        self.nr_cooks = nr_cooks
        self.nr_ovens = nr_ovens
        self.nr_stoves = nr_stoves
        self.order_list = PriorityQueue()

        self.cooks = [Cook(cook_id, cook['Rank'], cook['Proficiency'], cook['name'], cook['catch-phrase'], self)
                      for cook_id, cook in enumerate(COOKS)]
        self.stoves = [Stove(stove_id) for stove_id in range(nr_stoves)]
        self.ovens = [Oven(oven_id) for oven_id in range(nr_ovens)]

        # self.order_list_lock = threading.Lock()

    def run_test(self):
        for cook in self.cooks:
            # also each cook receives number of threads equal to their proficiency
            for _ in range(cook.proficiency):
                threading.Thread(target=cook.start_cooking, args=(self.order_list.queue,)).start()

        while True:
            for priority, order in self.order_list.queue:
                if order.is_finished():
                    cooking_end_time = int(time.time())
                    order.cooking_time = cooking_end_time - order.register_order_time
                    self.order_list.queue.remove((priority, order))
                    send_order_for_distribution(order)

    def save_order(self, order):

        order_id = order['order_id']
        table_id = order['table_id']
        waiter_id = order['waiter_id']
        items = order['items']
        priority = order['priority']
        max_wait = order['max_wait']
        pick_up_time = order['pick_up_time']
        register_order_time = int(time.time())

        order = Order(order_id, table_id, waiter_id, items, int(priority), int(max_wait), pick_up_time,
                      register_order_time)
        logger.warning(f'Order {order_id} put on order list')
        self.order_list.put((-order.priority, order))

    def get_available_apparatus(self, name):
        if name == 'oven':
            for oven in self.ovens:
                if oven.is_available:
                    oven.lock.acquire()
                    oven.busy()
                    return oven
        elif name == 'stove':
            for stove in self.stoves:
                if stove.is_available:
                    stove.lock.acquire()
                    stove.busy()
                    return stove
        return None
