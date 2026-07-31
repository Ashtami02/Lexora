from pydantic import BaseModel


class EvidenceRequest(BaseModel):

    session_id: str

    document_analysis: dict
    
    
    