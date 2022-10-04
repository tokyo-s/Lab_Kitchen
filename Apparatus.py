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

    def use(self, food):
        threading.Thread(target=self.prepare_food, args=(food,)).start()

    def prepare_food(self, food):
        logger.warning(f'Oven {self.oven_id} preparing food {food.item_id}, order {food.order_id}')
        time.sleep(food.preparation_time * TIME_UNIT / 1000)

        self.available()
        logger.warning(f'Oven {self.oven_id} prepared food {food.item_id}, order {food.order_id}')

    def busy(self):
        self.is_available = False

    def available(self):
        self.is_available = True


class Stove:
    def __init__(self, stove_id):
        self.stove_id = stove_id
        self.is_available = True
        self.lock = threading.Lock()

    def use(self, food):
        threading.Thread(target=self.prepare_food, args=(food,)).start()

    def prepare_food(self, food):
        logger.warning(f'Stove {self.stove_id} preparing food {food.item_id}, order {food.order_id}')
        time.sleep(food.preparation_time * TIME_UNIT / 1000)

        self.available()
        logger.warning(f'Stove {self.stove_id} prepared food {food.item_id}, order {food.order_id}')

    def busy(self):
        self.is_available = False

    def available(self):
        self.is_available = True
