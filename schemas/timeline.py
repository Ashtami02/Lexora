from pydantic import BaseModel
from typing import List, Any


class TimelineRequest(BaseModel):

    issue: str

    country: str

    state: str

    recommended_option: str

    recommendation_reason: str = ""

    required_documents: List[str] = []

    next_steps: List[str] = []

    action_plan: List[Any] = []