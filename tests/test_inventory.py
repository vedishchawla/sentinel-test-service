import pytest
from src.inventory import InventoryService

def test_inventory_deduction():
    service = InventoryService()
    service.set_stock("item_1", 10)
    assert service.process_order("item_1", 3) is True
    assert service.stock["item_1"] == 7
