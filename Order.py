class Order:
    def __init__(self, order_id, table_id, waiter_id, items, priority, max_wait, pick_up_time):
        self.order_id = order_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.items = items
        self.priority = priority
        self.max_wait = max_wait
        self.pick_up_time = pick_up_time

        self.finished = False
        self.taken = False

    def is_finished(self):
        return self.finished
