from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from appp.services.legal_ai import legal_ai

router = APIRouter()


class LegalAdvisorRequest(BaseModel):
    session_id: str
    question: str
    country: str
    location: str
    category: str
    language: str = "English"


# -----------------------------
# Existing JSON Endpoint
# -----------------------------

@router.post("/ask")
def ask_legal_question(request: LegalAdvisorRequest):

    return legal_ai.ask(
        session_id=request.session_id,
        question=request.question,
        country=request.country,
        location=request.location,
        category=request.category,
        language=request.language,
    )


