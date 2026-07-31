from collections import defaultdict
from typing import List, Dict


class SessionManager:

    def __init__(self):
        self.sessions = defaultdict(list)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content
            }
        )

    def get_history(
        self,
        session_id: str
    ) -> List[Dict]:

        return self.sessions.get(session_id, [])

    def clear_session(
        self,
        session_id: str
    ):

        if session_id in self.sessions:
            del self.sessions[session_id]


session_manager = SessionManager()