from Food import Food
from config import MENU


class Order:
    def __init__(self, order_id, table_id, waiter_id, items, priority, max_wait, pick_up_time):
        self.order_id = order_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.items = items
        self.priority = priority
        self.max_wait = max_wait
        self.pick_up_time = pick_up_time

        self.cooking_time = 0
        self.cooking_details = []
        self.food_items = [Food(self.order_id, item_id, MENU[item_id-1]['preparation-time'],
                                MENU[item_id-1]['complexity']) for item_id in self.items]
        self.nr_foods_prepared = 0

    def is_finished(self):
        for food in self.food_items:
            if not food.is_finished():
                return False
        return True

    def __lt__(self, other):
        self_priority = (self.priority, self.order_id)
        other_priority = (other.priority, other.order_id)
        return self_priority < other_priority
