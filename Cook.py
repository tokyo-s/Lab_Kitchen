import time
from config import TIME_UNIT
import logging

logger = logging.getLogger(__name__)


class Cook:
    def __init__(self, cook_id, rank, proficiency):
        self.cook_id = cook_id
        self.rank = rank
        self.proficiency = proficiency

    def start_cooking(self, order_list):

        while True:
            for order in order_list:
                if not order.taken:
                    order.taken = True
                    for food_idx, food in enumerate(order.food_items):
                        food.lock.aquire()
                        if not food.is_finished():
                            if food.complexity <= self.rank:
                                logger.warning(f'Cook {self.cook_id} started preparing food {food_idx}')
                                time.sleep(food.preparation_time * TIME_UNIT / 1000)
                                order.nr_foods_prepared += 1
                                logger.warning(f'Cook {self.cook_id} prepared food {food_idx}, order ready on '
                                               f'{int(order.nr_foods_prepared/len(order.items)*100)}%')
                            else:
                                logger.warning(f"Cook's {self.cook_id} rank lower than food {food_idx} complexity, "
                                               f'food not taken by the cook')
                        food.lock.release()
                    order.finished = True
                    order.cooking_time = food.preparation_time
