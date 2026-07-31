from typing import Optional, Literal
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):

    question: Optional[str] = Field(
        default=None,
        description="User's legal query"
    )

    country: Literal["India", "USA"]

    location: str

    category: Literal[
        "Rent & Eviction",
        "Bail & Arrest"
    ]

    language: str = "English"

    input_type: Literal[
        "text",
        "voice",
        "document"
    ] = "text"

    session_id: Optional[str] = None