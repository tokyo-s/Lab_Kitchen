import threading


class Food:
    def __init__(self, order_id, item_id, preparation_time, complexity, cook_id=None, status='not taken'):
        self.order_id = order_id
        self.item_id = item_id
        self.preparation_time = preparation_time
        self.complexity = complexity
        self.cook_id = cook_id
        self.status = status
        self.lock = threading.Lock()

    def is_finished(self):
        return self.status == 'finished'

    def finished(self):
        self.status = 'finished'

    def taken(self):
        self.status = 'taken'

    def is_taken(self):
        return self.status == 'taken'
