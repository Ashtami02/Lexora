from typing import List
from pydantic import BaseModel


class Annotation(BaseModel):
    text: str
    severity: str
    type: str
    reason: str


class DocumentAnalysisResponse(BaseModel):
    summary: str

    document_type: str

    document_language: str

    risk_score: int

    risk_level: str

    important_parties: List[str]

    important_dates: List[str]

    key_rights: List[str]

    key_obligations: List[str]

    important_clauses: List[str]

    legal_risks: List[str]

    red_flags: List[str]

    missing_information: List[str]

    recommended_actions: List[str]

    questions_to_ask: List[str]

    annotations: List[Annotation]

    confidence: float

    disclaimer: str

    highlighted_pdf: str | None = None

    success: bool