from fastapi import APIRouter

from appp.schemas.doc_generator import DocumentRequest
from appp.services.document_generator import document_generator

router = APIRouter()


@router.post("/generate")
def generate_document(request: DocumentRequest):

    return document_generator.generate(
        request.document_type,
        request.country,
        request.state,
        request.language,
        request.description,
    )