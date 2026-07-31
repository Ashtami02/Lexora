from fastapi import APIRouter, HTTPException

from appp.schemas.request import AnalyzeRequest
from appp.schemas.response import AnalyzeResponse

from appp.services.rag_client import rag_client
from appp.prompt.prompt_builder import build_prompt
from appp.services.gemma import gemma_service
from appp.services.lawyer_recommendation import find_lawyers

router = APIRouter(
    prefix="/analyze",
    tags=["AI Legal Assistant"]
)

@router.post("/", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):

    try:

        retrieved_context = rag_client.retrieve_context(
            question=request.question,
            country=request.country,
            location=request.location,
            category=request.category,
            k=5
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"RAG Error: {str(e)}"
        )

    prompt = build_prompt(
        question=request.question,
        language=request.language,
        context=retrieved_context
    )

    ai_response = gemma_service.analyze_case(prompt)

    if ai_response.get("lawyer_needed"):

        lawyers = find_lawyers(
            country=request.country,
            city=request.location,
            specialization=ai_response["lawyer_specialization"],
            language=request.language
        )

        ai_response["recommended_lawyers"] = lawyers

    else:

        ai_response["recommended_lawyers"] = []

    return ai_response