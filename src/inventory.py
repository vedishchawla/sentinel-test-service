class InventoryService:
    def __init__(self):
        self.stock = {}

    def set_stock(self, item_id: str, quantity: int):
        self.stock[item_id] = quantity

    def process_order(self, item_id: str, quantity: int) -> bool:
        # BUG: No thread-safe locking or atomic check causes race condition and negative inventory
        current = self.stock.get(item_id, 0)
        if current >= quantity:
            self.stock[item_id] = current - quantity
            return True
        return False
