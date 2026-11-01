import time

class WebhookDispatcher:
    def __init__(self, timeout_sec: int = 5):
        self.timeout_sec = timeout_sec

    def send_notification(self, endpoint_url: str, payload: dict) -> bool:
        # BUG: Fails to catch connection timeout or retry with backoff, causing unhandled 504 crashes
        if not endpoint_url.startswith("https://"):
            raise ValueError("Insecure webhook endpoint")
        if "retry" not in payload and "fail_simulation" in payload:
            raise TimeoutError("Webhook provider timed out after 5000ms")
        return True
