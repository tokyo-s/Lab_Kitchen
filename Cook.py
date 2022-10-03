import time
from config import TIME_UNIT
import logging

logger = logging.getLogger(__name__)


class Cook:
    def __init__(self, cook_id, rank, proficiency, name, catch_phrase, kitchen):
        self.cook_id = cook_id
        self.rank = rank
        self.proficiency = proficiency
        self.name = name
        self.catch_phrase = catch_phrase
        self.kitchen = kitchen

    def start_cooking(self, order_list):

        while True:
            for _, order in order_list:
                if not order.is_finished():
                    for food_idx, food in enumerate(order.food_items):
                        if not food.is_taken():
                            food.lock.acquire()
                            if not food.is_finished():
                                if food.complexity <= self.rank:
                                    apparatus = None
                                    if food.cooking_apparatus:
                                        apparatus = self.kitchen.get_available_apparatus(food.cooking_apparatus)
                                        if not apparatus:
                                            food.lock.release()
                                            continue
                                    food.taken()
                                    logger.warning(f'Cook {self.name} started preparing food {food_idx} from {food.order_id}')
                                    order.cooking_details.append({'food_id': food.item_id, 'cook_id': self.cook_id})

                                    if apparatus:
                                        apparatus.prepare_food(food)
                                    else:
                                        time.sleep(food.preparation_time * TIME_UNIT / 1000)
                                        food.finished()
                                        order.nr_foods_prepared += 1
                                        logger.warning(f'Cook {self.name} prepared food {food_idx}, order {food.order_id} '
                                                       f'ready on {int(order.nr_foods_prepared/len(order.items)*100)}%')
                                else:
                                    logger.warning(f"Cook {self.name}'s rank {self.rank} lower than food {food_idx} "
                                                   f"from {food.order_id} complexity {food.complexity}, "
                                                   f'food not taken by the cook')
                            food.lock.release()

            time.sleep(0.01 * TIME_UNIT / 1000)
