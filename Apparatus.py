import threading
import time
from config import TIME_UNIT
import logging
import threading

logger = logging.getLogger(__name__)


class Oven:
    def __init__(self, oven_id):
        self.oven_id = oven_id
        self.is_available = True
        self.lock = threading.Lock()

    def use(self, food, food_idx):
        threading.Thread(target=self.prepare_food, args=(food,food_idx)).start()

    def prepare_food(self, food, food_idx):
        logger.warning(f'Oven {self.oven_id} preparing food {food_idx}, order {food.order_id}')
        time.sleep(food.preparation_time * TIME_UNIT / 1000)
        self.available()
        self.lock.release()
        logger.warning(f'Oven {self.oven_id} prepared food {food_idx}, order {food.order_id}')

    def busy(self):
        self.is_available = False

    def available(self):
        self.is_available = True


class Stove:
    def __init__(self, stove_id):
        self.stove_id = stove_id
        self.is_available = True
        self.lock = threading.Lock()

    def use(self, food, food_idx):
        threading.Thread(target=self.prepare_food, args=(food,food_idx)).start()

    def prepare_food(self, food, food_idx):
        logger.warning(f'Stove {self.stove_id} preparing food {food_idx}, order {food.order_id}')
        time.sleep(food.preparation_time * TIME_UNIT / 1000)
        self.available()
        self.lock.release()
        logger.warning(f'Stove {self.stove_id} prepared food {food_idx}, order {food.order_id}')

    def busy(self):
        self.is_available = False

    def available(self):
        self.is_available = True
