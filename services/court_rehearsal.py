from uuid import uuid4

from appp.database.court_memory import court_memory
from appp.services.speech import speech_service

from appp.prompt.court_prompt import (
    COURT_SYSTEM_PROMPT,
    COURT_START_PROMPT,
    COURT_CONTINUE_PROMPT,
    COURT_EVALUATION_PROMPT,
    COURT_CROSS_EXAM_PROMPT,
    COURT_CLOSING_ARGUMENT_PROMPT,
)

from appp.services.gemma import gemma_service


class CourtRehearsalService:

    # ----------------------------------
    # Start Hearing
    # ----------------------------------

    def start_session(
        self,
        country,
        state,
        language,
        case_type,
        role,
        description,
    ):

        session_id = str(uuid4())

        court_memory.create_session(
            session_id=session_id,
            country=country,
            state=state,
            language=language,
            case_type=case_type,
            role=role,
            description=description,
        )

        prompt = COURT_START_PROMPT.format(
            country=country,
            state=state,
            language=language,
            case_type=case_type,
            role=role,
            description=description,
        )

        result = gemma_service.generate_json(
            prompt=prompt,
            system_prompt=COURT_SYSTEM_PROMPT,
        )

        if "raw_response" in result:
            return result

        court_memory.add_message(
            session_id,
            "judge",
            result["judge_message"],
        )

        court_memory.increment_question(session_id)

        return {
            "success": True,
            "session_id": session_id,
            **result,
        }

    # ----------------------------------
    # Continue Hearing
    # ----------------------------------

    def respond(
        self,
        session_id,
        answer=None,
        audio_path=None,
    ):
        # ----------------------------------
        # Voice Answer Processing
        # ----------------------------------

        speech_analysis = None

        if audio_path:

            speech_analysis = speech_service.analyze(
                audio_path
            )

            if speech_analysis["processing_status"] == "failed":

                return speech_analysis

            # Use Whisper transcript as the answer
            answer = speech_analysis["transcript"]
            
        # ----------------------------------
        # Build Speech Analysis Context
        # ----------------------------------

        speech_context = ""

        if speech_analysis:

            speech_context = f"""
        Speech Analysis:

        Duration:
        {speech_analysis.get("duration", 0)} seconds

        Words Per Minute:
        {speech_analysis.get("words_per_minute", 0)}

        Filler Words:
        {speech_analysis.get("filler_words", 0)}

        Voice Energy:
        {speech_analysis.get("voice_energy", 0)}

        Long Pauses:
        {speech_analysis.get("long_pauses", 0)}
        """

        session = court_memory.get_session(session_id)
        # ----------------------------------
        # Build Evidence Context
        # ----------------------------------

        evidence_context = ""

        for index, evidence in enumerate(session["evidence"], start=1):

            evidence_context += f"""

        Evidence {index}

        Summary:
        {evidence.get("summary","")}

        Important Dates:
        {evidence.get("important_dates",[])}

        Important Parties:
        {evidence.get("important_parties",[])}

        Legal Risks:
        {evidence.get("legal_risks",[])}

        Important Clauses:
        {evidence.get("important_clauses",[])}

        Annotations:
        {evidence.get("annotations",[])}

        """
        # ----------------------------------
        # Build Facts Context
        # ----------------------------------

        facts_context = ""

        for key, value in session["facts"].items():

            facts_context += f"{key}: {value}\n"

        if session is None:

            return {
                "success": False,
                "message": "Session not found."
            }

        court_memory.add_message(
            session_id,
            "user",
            answer,
        )

        history = ""

        for message in session["messages"]:

            history += (
                f'{message["role"].capitalize()}: '
                f'{message["message"]}\n'
            )

        stage = session["stage"]

        if stage == "preliminary":

        

            prompt = COURT_CONTINUE_PROMPT.format(
                language=session["language"],
                country=session["country"],
                state=session["state"],
                case_type=session["case_type"],
                role=session["role"],
                history=history,
                answer=answer,
                evidence=evidence_context,
                speech=speech_context,
                question_number=session["question_count"],
            )

        elif stage == "cross_examination":

            prompt = COURT_CROSS_EXAM_PROMPT.format(
                language=session["language"],
                country=session["country"],
                state=session["state"],
                history=history,
                answer=answer,
                evidence=evidence_context,
                speech=speech_context,
            )

        elif stage == "closing_arguments":

            prompt = COURT_CLOSING_ARGUMENT_PROMPT.format(
                language=session["language"],
                country=session["country"],
                state=session["state"],
                history=history,
                answer=answer,
                evidence=evidence_context,
                speech=speech_context,
            )

        else:

            prompt = COURT_CONTINUE_PROMPT.format(
                language=session["language"],
                history=history,
                answer=answer,
                evidence=evidence_context,
                speech=speech_context,
    )

        result = gemma_service.generate_json(
            prompt=prompt,
            system_prompt=COURT_SYSTEM_PROMPT,
        )

        if "raw_response" in result:
            return result

        court_memory.add_message(
            session_id,
            "judge",
            result["judge_message"],
        )

        court_memory.increment_question(session_id)

        court_memory.add_score(
            session_id,
            result.get("score", 0),
        )

        return self.handle_stage(
            session_id,
            result,
        )

    # ----------------------------------
    # Stage Handler
    # ----------------------------------

    def handle_stage(
        self,
        session_id,
        result,
    ):

        session = court_memory.get_session(session_id)

        question_count = session["question_count"]

        if question_count >= 10:

            court_memory.set_stage(
                session_id,
                "evaluation",
            )

            return self.generate_mid_hearing_report(
                session_id,
            )

        result["success"] = True

        return result

    # ----------------------------------
    # Mid Hearing Report
    # ----------------------------------

    # ----------------------------------
    # Mid Hearing Report
    # ----------------------------------

    def generate_mid_hearing_report(
        self,
        session_id,
    ):

        session = court_memory.get_session(session_id)

        conversation = ""

        for message in session["messages"]:

            conversation += (
                f'{message["role"].capitalize()}: '
                f'{message["message"]}\n'
            )

        prompt = COURT_EVALUATION_PROMPT.format(

            conversation=conversation,

            language=session["language"],

            country=session["country"],

            state=session["state"],
        )

        result = gemma_service.generate_json(

            prompt=prompt,

            system_prompt=COURT_SYSTEM_PROMPT,
        )

        if "raw_response" in result:

            return {
                "success": False,
                "message": "Evaluation failed.",
                "raw_response": result["raw_response"],
            }

        result["success"] = True

        result["stage"] = "evaluation"

        return result

    def change_mode(
    self,
    session_id,
    mode,
):

        session = court_memory.get_session(session_id)

        if session is None:

            return {
                "success": False,
                "message": "Session not found."
            }

        court_memory.set_mode(
            session_id,
            mode,
        )

        if mode == "judge":

            court_memory.set_stage(
                session_id,
                "preliminary",
            )

            message = (
                "The hearing will continue before the Court."
            )

        elif mode == "cross":

            court_memory.set_stage(
                session_id,
                "cross_examination",
            )

            message = (
                "Cross Examination has begun. The opposing counsel will now question you."
            )

        elif mode == "closing":

            court_memory.set_stage(
                session_id,
                "closing_arguments",
            )

            message = (
                "Please present your closing argument to the Court."
            )

        else:

            court_memory.set_stage(
                session_id,
                "finished",
            )

            message = (
                "The Court session has ended."
            )

        return {

            "success": True,

            "mode": mode,

            "stage": session["stage"],

            "judge_message": message,
        }
    # ----------------------------------
    # Add Evidence
    # ----------------------------------

    def add_evidence(
        self,
        session_id,
        document,
    ):

        session = court_memory.get_session(session_id)

        if session is None:

            return {
                "success": False,
                "message": "Court session not found."
            }

        court_memory.add_evidence(
            session_id,
            document,
        )

        return {

            "success": True,

            "message": "Evidence added successfully.",

            "total_documents": len(
                session["evidence"]
            )
        }

court_rehearsal_service = CourtRehearsalService()