from fastapi import APIRouter, Query

from appp.services.lawyer_recommendation import (
    lawyer_recommendation_service,
)


router = APIRouter(
    prefix="/lawyers",
    tags=["Lawyers"],
)


@router.get("/recommend")
def recommend_lawyers(

    country: str = Query(None),

    city: str = Query(None),

    specialization: str = Query(None),

    language: str = Query(None),

    top_k: int = Query(3),

):

    return lawyer_recommendation_service.recommend(

        country=country,

        city=city,

        specialization=specialization,

        language=language,

        top_k=top_k,

    )