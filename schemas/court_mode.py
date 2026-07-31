from pydantic import BaseModel


class CourtModeRequest(BaseModel):

    session_id: str

    mode: str