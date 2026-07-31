from typing import Dict


class CourtMemory:

    def __init__(self):

        self.sessions: Dict[str, dict] = {}

    # ----------------------------------
    # Create Session
    # ----------------------------------

    def create_session(
        self,
        session_id: str,
        country: str,
        state: str,
        language: str,
        case_type: str,
        role: str,
        description: str,
    ):

        self.sessions[session_id] = {

            "session_id": session_id,

            "country": country,

            "state": state,

            "language": language,

            "case_type": case_type,

            "role": role,

            "description": description,

            # Current Stage
            "stage": "opening",

            # Current Mode
            "mode": "judge",

            # Question Counter
            "question_count": 0,

            # Conversation
            "messages": [],
            
            "evidence": [],
        }

    # ----------------------------------
    # Add Message
    # ----------------------------------

    def add_message(
        self,
        session_id: str,
        role: str,
        message: str,
    ):

        self.sessions[session_id]["messages"].append(
            {
                "role": role,
                "message": message,
            }
        )

    # ----------------------------------
    # Increment Question Count
    # ----------------------------------

    def increment_question(
        self,
        session_id: str,
    ):

        self.sessions[session_id]["question_count"] += 1

    # ----------------------------------
    # Change Stage
    # ----------------------------------

    def set_stage(
        self,
        session_id: str,
        stage: str,
    ):

        self.sessions[session_id]["stage"] = stage

    # ----------------------------------
    # Change Mode
    # ----------------------------------

    def set_mode(
        self,
        session_id: str,
        mode: str,
    ):

        self.sessions[session_id]["mode"] = mode

    # ----------------------------------
    # Get Session
    # ----------------------------------

    def get_session(
        self,
        session_id: str,
    ):

        return self.sessions.get(session_id)

    # ----------------------------------
    # Delete Session
    # ----------------------------------

    def delete_session(
        self,
        session_id: str,
    ):

        if session_id in self.sessions:
            del self.sessions[session_id]

    # ----------------------------------
    # Add Evidence
    # ----------------------------------

    def add_evidence(
        self,
        session_id,
        evidence,
    ):

        self.sessions[session_id]["evidence"].append(
            evidence
        )


    # ----------------------------------
    # Get Evidence
    # ----------------------------------

    def get_evidence(
        self,
        session_id,
    ):

        return self.sessions[session_id]["evidence"]

court_memory = CourtMemory()