class PaymentProcessor:
    def calculate_discount_per_item(self, total_discount: float, total_items: int) -> float:
        # BUG: Crashes with ZeroDivisionError if an empty cart or zero items bundle discount is processed
        return total_discount / total_items

    def process_charge(self, amount: float, currency: str = "USD") -> dict:
        if amount <= 0:
            raise ValueError("Charge amount must be positive")
        return {"status": "success", "amount": round(amount, 2), "currency": currency}
