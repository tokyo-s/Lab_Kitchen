import threading
import time
from config import TIME_UNIT
import logging

logger = logging.getLogger(__name__)


class Oven:
    def __init__(self, oven_id):
        self.oven_id = oven_id
        self.is_available = True

    def use(self, food):
        self.is_available = False
        threading.Thread(target=self.prepare_food, args=(food,)).start()

    def prepare_food(self, food):
        time.sleep(food.preparation_time * TIME_UNIT / 1000)
        food.finished()
        self.is_available = True

        logger.warning(f'Oven {self.oven_id} prepared food {food.item_id}, order {food.order_id}')


class Stove:
    def __init__(self, stove_id):
        self.stove_id = stove_id
        self.is_available = True

    def use(self, food):
        self.is_available = False
        threading.Thread(target=self.prepare_food, args=(food,)).start()

    def prepare_food(self, food):
        time.sleep(food.preparation_time * TIME_UNIT / 1000)
        food.finished()
        self.is_available = True

        logger.warning(f'Stove {self.stove_id} prepared food {food.item_id}, order {food.order_id}')

