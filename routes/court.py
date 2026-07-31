from fastapi import APIRouter
from appp.schemas.court_mode import CourtModeRequest
from appp.schemas.evidence import EvidenceRequest

from appp.schemas.court import (
    CourtStartRequest,
    CourtResponseRequest,
    CourtEndRequest,
)

from appp.services.court_rehearsal import (
    court_rehearsal_service,
)

router = APIRouter()


# ----------------------------------
# Start Court Session
# ----------------------------------

@router.post("/start")
def start_session(request: CourtStartRequest):

    return court_rehearsal_service.start_session(
        country=request.country,
        state=request.state,
        language=request.language,
        case_type=request.case_type,
        role=request.role,
        description=request.description,
    )


# ----------------------------------
# Respond
# ----------------------------------

@router.post("/respond")
def respond(request: CourtResponseRequest):

    return court_rehearsal_service.respond(
        session_id=request.session_id,
        answer=request.answer,
        language=request.language,
    )


# ----------------------------------
# End Session
# ----------------------------------

@router.post("/end")
def end_session(request: CourtEndRequest):

    return court_rehearsal_service.end_session(
        session_id=request.session_id,
    )
    
@router.post("/change-mode")
def change_mode(request: CourtModeRequest):

    return court_rehearsal_service.change_mode(
        session_id=request.session_id,
        mode=request.mode,
    )

# ----------------------------------
# Add Evidence
# ----------------------------------

@router.post("/add-evidence")
def add_evidence(request: EvidenceRequest):

    return court_rehearsal_service.add_evidence(
        session_id=request.session_id,
        document=request.document_analysis,
    )