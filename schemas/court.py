from pydantic import BaseModel


class CourtStartRequest(BaseModel):

    country: str
    state: str
    language: str
    case_type: str
    role: str
    description: str


class CourtResponseRequest(BaseModel):

    session_id: str
    language: str
    answer: str


class CourtEndRequest(BaseModel):

    session_id: str