from typing import List, Optional
from pydantic import BaseModel


class LegalOption(BaseModel):
    title: str
    description: str
    estimated_time: str
    estimated_cost: str
    difficulty: str


class Lawyer(BaseModel):
    name: str
    specialization: str
    city: str
    language: List[str]
    experience: int
    consultation_fee: str
    rating: float


class Source(BaseModel):
    pdf_url: Optional[str] = None
    page: Optional[int]
    section: Optional[str]


class AnalyzeResponse(BaseModel):

    issue: str

    severity: str

    confidence: float

    rights: str

    explanation: str

    options: List[LegalOption]

    recommended_option: str

    recommendation_reason: str

    timeline: List[str]

    estimated_cost: str

    required_documents: List[str]

    next_steps: List[str]

    lawyer_needed: bool

    lawyer_specialization: Optional[str]

    recommended_lawyers: List[Lawyer]

    sources: List[Source]