from Cook import Cook
from Order import Order
from config import *
import threading
import logging
import requests
from queue import PriorityQueue

logger = logging.getLogger(__name__)
DINNING_HALL_URL = "http://dinning-hall-container:8001"


def send_order_for_distribution(order):
    logger.warning('Sending food to dining hall')
    order_json = dict(order.__dict__)
    del order_json['food_items']
    del order_json['nr_foods_prepared']
    requests.post(f'{DINNING_HALL_URL}/distribution', json=order_json)


class Kitchen:
    def __init__(self, nr_cooks=NR_COOKS, nr_ovens=NR_OVENS, nr_stoves=NR_STOVES):
        self.nr_cooks = nr_cooks
        self.nr_ovens = nr_ovens
        self.nr_stoves = nr_stoves
        self.order_list = PriorityQueue()

        self.cooks = [Cook(cook_id, cook['Rank'], cook['Proficiency']) for cook_id, cook in enumerate(COOKS)]

        # self.order_list_lock = threading.Lock()

    def run_test(self):
        for cook in self.cooks:
            # also each cook receives number of threads equal to their proficiency
            for _ in range(cook.proficiency):
                threading.Thread(target=cook.start_cooking, args=(self.order_list.queue,)).start()

        while True:
            for priority, order in self.order_list.queue:
                if order.is_finished():
                    send_order_for_distribution(order)
                    self.order_list.queue.remove((priority, order))

    def save_order(self, order):

        order_id = order['order_id']
        table_id = order['table_id']
        waiter_id = order['waiter_id']
        items = order['items']
        priority = order['priority']
        max_wait = order['max_wait']
        pick_up_time = order['pick_up_time']

        order = Order(order_id, table_id, waiter_id, items, int(priority), int(max_wait), float(pick_up_time))
        logger.warning(f'Order {order_id} put on order list')
        self.order_list.put((-order.priority, order))
        # self.order_list.append(order)
