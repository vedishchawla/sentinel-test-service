import pytest
from src.inventory import InventoryService
from src.payment import PaymentProcessor
from src.auth import AuthService
from src.session_manager import SessionManager
from src.webhook import WebhookDispatcher

def test_inventory_normal():
    inv = InventoryService()
    inv.set_stock("item_1", 10)
    assert inv.process_order("item_1", 4) is True
    assert inv.stock["item_1"] == 6

def test_payment_normal():
    pay = PaymentProcessor()
    res = pay.process_charge(99.99)
    assert res["status"] == "success"

def test_auth_normal():
    auth = AuthService()
    res = auth.parse_auth_header("Bearer token_abc123")
    assert res["token"] == "token_abc123"

def test_session_normal():
    mgr = SessionManager()
    sid = mgr.create_session("usr_1", {"role": "admin"})
    assert mgr.get_session(sid) == {"role": "admin"}

def test_webhook_normal():
    wb = WebhookDispatcher()
    assert wb.send_notification("https://api.partner.com/notify", {"event": "order_created"}) is True
