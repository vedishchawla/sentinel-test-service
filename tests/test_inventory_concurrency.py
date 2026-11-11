import threading
import pytest
from src.inventory import InventoryService

@pytest.fixture
def inventory():
    svc = InventoryService()
    # start with a known stock level for item 'item1'
    svc.stock['item1'] = 10
    return svc


def test_fix_original_bug_concurrent_orders(inventory):
    """should fix the original bug"""
    item_id = 'item1'
    order_quantity = 3
    # We will launch 5 threads, each trying to order 3 units (total demand 15 > stock 10)
    success_flags = []
    def attempt_order():
        result = inventory.process_order(item_id, order_quantity)
        success_flags.append(result)

    threads = [threading.Thread(target=attempt_order) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # At most floor(10/3) = 3 orders should have succeeded
    assert sum(success_flags) == 3
    # Stock must never become negative
    assert inventory.stock[item_id] >= 0
    # Remaining stock should equal initial - successful_orders * quantity
    assert inventory.stock[item_id] == 10 - 3 * order_quantity


def test_handle_zero_quantity_edge_case(inventory):
    """should handle edge case X"""
    item_id = 'item1'
    initial_stock = inventory.stock[item_id]
    # Ordering zero should be a no‑op but return True (treated as successful)
    result = inventory.process_order(item_id, 0)
    assert result is True
    # Stock must remain unchanged
    assert inventory.stock[item_id] == initial_stock


def test_sequential_orders_no_regression(inventory):
    """should not regress on Y"""
    item_id = 'item1'
    # First order within stock limits
    assert inventory.process_order(item_id, 4) is True
    assert inventory.stock[item_id] == 6
    # Second order exceeds remaining stock
    assert inventory.process_order(item_id, 7) is False
    # Stock must stay at 6 after failed attempt
    assert inventory.stock[item_id] == 6
    # A final valid order consumes the rest
    assert inventory.process_order(item_id, 6) is True
    assert inventory.stock[item_id] == 0


def test_negative_quantity_error_case(inventory):
    """should handle error case Z"""
    item_id = 'item1'
    initial_stock = inventory.stock[item_id]
    # The current implementation treats negative quantity as a failed order (does not modify stock)
    result = inventory.process_order(item_id, -5)
    assert result is False
    # Ensure stock is unchanged
    assert inventory.stock[item_id] == initial_stock
