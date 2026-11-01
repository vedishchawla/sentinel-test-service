class SessionManager:
    def __init__(self):
        # BUG: Unbounded global dictionary grows forever on every login, causing memory leak and OOM crash
        self.sessions = {}

    def create_session(self, user_id: str, session_data: dict) -> str:
        session_id = f"sess_{user_id}_{len(self.sessions) + 1}"
        self.sessions[session_id] = session_data  # Never cleaned up or capped
        return session_id

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)
