from pydantic import BaseModel


class DocumentRequest(BaseModel):

    document_type: str

    country: str

    state: str

    language: str

    description: str