from collections import OrderedDict

class SessionManager:
    def __init__(self):
        # BUG: Unbounded global dictionary grows forever on every login, causing memory leak and OOM crash
        self.sessions = OrderedDict()

    def create_session(self, user_id: str, session_data: dict) -> str:
        session_id = f"sess_{user_id}_{len(self.sessions) + 1}"
        self.sessions[session_id] = session_data  # Never cleaned up or capped
        # Evict oldest session if exceeding max size to prevent unbounded growth
        MAX_SESSIONS = 1000
        if len(self.sessions) > MAX_SESSIONS:
            self.sessions.popitem(last=False)
        return session_id

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)