from fastapi import APIRouter

from appp.schemas.timeline import (
    TimelineRequest
)

from appp.services.timeline import (
    timeline_service
)


router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
)


@router.post("/generate")
def generate_timeline(
    request: TimelineRequest,
):

    return timeline_service.generate_timeline(

        issue=request.issue,

        country=request.country,

        state=request.state,

        recommended_option=
            request.recommended_option,

        recommendation_reason=
            request.recommendation_reason,

        required_documents=
            request.required_documents,

        next_steps=
            request.next_steps,

        action_plan=
            request.action_plan,

    )