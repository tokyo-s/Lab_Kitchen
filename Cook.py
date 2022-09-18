import time

class Cook:
    def __init__(self, cook_id):
        self.cook_id = cook_id

    def start_cooking(self, order_list):
        while True:
            for order in order_list:
                if not order.taken:
                    order.taken = True
                    time.sleep(5)
                    order.finished = True

