import json

from appp.services.rag_client import rag_client
from appp.services.gemma import gemma_service

from appp.prompt.prompt_builder import build_prompt

from appp.database.chat_memory import chat_memory

from appp.lawyer_database.crud import get_recommended_lawyers


class LegalAI:

    def ask(
        self,
        session_id: str,
        question: str,
        country: str,
        location: str,
        category: str,
        language: str = "English",
        k: int = 5,
    ):

        # ----------------------------------
        # Previous Conversation
        # ----------------------------------

        history = chat_memory.get_history(session_id)

        history_text = ""

        for msg in history:

            history_text += f"""
{msg['role'].capitalize()}:
{msg['message']}

"""

        # ----------------------------------
        # Retrieve Legal Context
        # ----------------------------------

        documents = rag_client.retrieve(
            question=question,
            country=country,
            location=location,
            category=category,
            k=k,
        )

        if not documents:

            return {
                "success": False,
                "message": "No relevant legal documents were found.",
            }

        # ----------------------------------
        # Build Context
        # ----------------------------------

        context = ""

        sources = []

        seen_sources = set()

        for doc in documents:

            context += f"""
Source: {doc['source']}
Page: {doc['page']}
Country: {doc['country']}
Location: {doc['location']}
Category: {doc['category']}

{doc['text']}

------------------------------------
"""

            key = (
                doc["source"],
                doc["page"],
            )

            if key not in seen_sources:

                seen_sources.add(key)

                sources.append(
                    {
                        "document": doc["source"],
                        "page": doc["page"],
                    }
                )

        # ----------------------------------
        # Build Prompt
        # ----------------------------------

        prompt = build_prompt(
            question=question,
            country=country,
            location=location,
            category=category,
            language=language,
            context=context,
            history=history_text,
        )

        # ----------------------------------
        # Ask Gemma
        # ----------------------------------

        response = gemma_service.analyze_case(prompt)

        # ----------------------------------
        # Convert JSON
        # ----------------------------------

        if isinstance(response, str):

            try:

                response = json.loads(response)

            except Exception:

                return {
                    "success": False,
                    "message": "Gemma returned invalid JSON.",
                    "raw_output": response,
                }

        # ----------------------------------
        # Attach Sources
        # ----------------------------------

        sources = []

        seen_sources = set()

        for doc in documents:

            key = (
                doc["source"],
                doc["page"],
            )

            if key not in seen_sources:

                seen_sources.add(key)

                sources.append(
                    {
                        "pdf_url": doc["pdf_url"],
                        "page": doc["page"],
                    }
                )

        response["sources"] = sources

        # ----------------------------------
        # Recommend Lawyers
        # ----------------------------------

        print("========== DEBUG ==========")
        print("lawyer_needed:", response.get("lawyer_needed"))
        print("specialization:", repr(response.get("lawyer_specialization")))
        print("location:", repr(location))
        print("===========================")

        if response.get("lawyer_needed"):

            specialization = response.get("lawyer_specialization", "").strip()

            lawyers = get_recommended_lawyers(
                practice_area=specialization,
                state=location.strip(),
            )

            print("Lawyers found:", lawyers)

            response["recommended_lawyers"] = lawyers

        else:
            response["recommended_lawyers"] = []

        # ----------------------------------
        # Save Conversation
        # ----------------------------------

        chat_memory.add_message(
            session_id=session_id,
            role="user",
            message=question,
        )

        chat_memory.add_message(
            session_id=session_id,
            role="assistant",
            message=json.dumps(response),
        )

        # ----------------------------------
        # Success
        # ----------------------------------

        response["success"] = True

        return response


legal_ai = LegalAI()