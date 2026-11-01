import threading
import pytest
from src.inventory import InventoryService

@pytest.fixture
def inventory():
    svc = InventoryService()
    # Initialize stock for tests
    svc.stock = {
        "itemA": 10,
        "itemB": 5,
    }
    return svc


def test_fix_original_bug_concurrent_deductions(inventory):
    """should fix the original bug"""
    item_id = "itemA"
    order_qty = 3
    threads = []
    results = []

    def worker():
        success = inventory.process_order(item_id, order_qty)
        results.append(success)

    # Launch 5 threads (total demand 15 > stock 10)
    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Only floor(10/3)=3 orders should succeed
    assert results.count(True) == 3
    # Stock must never become negative
    assert inventory.stock[item_id] >= 0
    # Final stock should be 10 - 3*3 = 1
    assert inventory.stock[item_id] == 1


def test_handle_zero_quantity_edge_case(inventory):
    """should handle edge case X"""
    item_id = "itemA"
    initial_stock = inventory.stock[item_id]
    # Ordering zero should be a no‑op but return True (treated as successful)
    assert inventory.process_order(item_id, 0) is True
    assert inventory.stock[item_id] == initial_stock


def test_insufficient_stock_returns_false_no_regression(inventory):
    """should not regress on Y"""
    item_id = "itemB"
    # Stock is 5, request 10
    assert inventory.process_order(item_id, 10) is False
    # Stock must remain unchanged
    assert inventory.stock[item_id] == 5


def test_concurrent_orders_different_items_do_not_interfere(inventory):
    """should handle error case Z"""
    threads = []
    results = []

    def worker(item, qty):
        results.append((item, inventory.process_order(item, qty)))

    # Two items, each with enough stock for two orders
    for _ in range(2):
        threads.append(threading.Thread(target=worker, args=("itemA", 2)))
        threads.append(threading.Thread(target=worker, args=("itemB", 2)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All orders should succeed because stock permits
    for item, success in results:
        assert success is True
    # Verify final stock values
    assert inventory.stock["itemA"] == 10 - 2 * 2  # 6
    assert inventory.stock["itemB"] == 5 - 2 * 2   # 1
