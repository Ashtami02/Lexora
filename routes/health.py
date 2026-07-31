from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["AI Legal Advisor"]
)


@router.get("/health")
def health():

    return {
        "status": "Backend Working"
    }