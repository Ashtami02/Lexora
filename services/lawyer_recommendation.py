from typing import List

LAWYERS = [
    {
        "name": "Advocate Rahul Sharma",
        "country": "India",
        "city": "Delhi",
        "specialization": "Rent & Eviction",
        "languages": ["English", "Hindi"],
        "experience": 12,
        "consultation_fee": "₹1500",
        "rating": 4.9,
    },
    {
        "name": "Advocate Priya Mehta",
        "country": "India",
        "city": "Delhi",
        "specialization": "Bail & Arrest",
        "languages": ["English", "Hindi"],
        "experience": 8,
        "consultation_fee": "₹1200",
        "rating": 4.8,
    },
    {
        "name": "John Williams",
        "country": "USA",
        "city": "New York",
        "specialization": "Rent & Eviction",
        "languages": ["English", "Spanish"],
        "experience": 15,
        "consultation_fee": "$200",
        "rating": 4.9,
    },
    {
        "name": "Emily Carter",
        "country": "USA",
        "city": "New York",
        "specialization": "Bail & Arrest",
        "languages": ["English"],
        "experience": 10,
        "consultation_fee": "$180",
        "rating": 4.7,
    },
]

from appp.lawyer_database.crud import find_lawyers


class LawyerRecommendationService:

    def recommend(
        self,
        country=None,
        city=None,
        specialization=None,
        language=None,
        top_k=3,
    ):

        lawyers = find_lawyers(
            country=country,
            city=city,
            specialization=specialization,
            language=language,
            top_k=top_k,
        )

        return {
            "success": True,
            "count": len(lawyers),
            "lawyers": lawyers,
        }


lawyer_recommendation_service = (
    LawyerRecommendationService()
)
def find_lawyers(
    country: str,
    city: str,
    specialization: str,
    language: str,
    top_k: int = 3,
) -> List[dict]:

    matches = []

    for lawyer in LAWYERS:

        if lawyer["country"] != country:
            continue

        if lawyer["city"] != city:
            continue

        if lawyer["specialization"] != specialization:
            continue

        if language not in lawyer["languages"]:
            continue

        matches.append(lawyer)

    matches.sort(key=lambda x: x["rating"], reverse=True)

    return matches[:top_k]



