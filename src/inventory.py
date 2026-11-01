import threading

class InventoryService:
    def __init__(self):
        self.stock = {}
        self._lock = threading.Lock()

    def set_stock(self, item_id: str, quantity: int):
        self.stock[item_id] = quantity

    def process_order(self, item_id: str, quantity: int) -> bool:
        # BUG: No lock or check before deduction causes race condition / negative stock
        with self._lock:
            current = self.stock.get(item_id, 0)
            if current >= quantity:
                self.stock[item_id] = current - quantity
                return True
            return False