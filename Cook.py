import time
from config import TIME_UNIT

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
                    time.sleep(5 * TIME_UNIT / 1000)

                    order.finished = True
                    order.cooking_time = 5
