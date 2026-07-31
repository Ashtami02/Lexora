class RecommendationService:

    def enhance(self, ai_response: dict):

        severity = ai_response.get("severity", "").lower()
        risk = ai_response.get("risk_level", "").lower()

        recommendation = {
            "priority": "Normal",
            "priority_color": "green",
            "estimated_response_time": "Within a few days",
            "show_emergency_banner": False,
            "action_card": {
                "title": "General Legal Guidance",
                "description": "Follow the recommended next steps."
            }
        }

        if severity == "high" or risk == "high":

            recommendation = {
                "priority": "Immediate",
                "priority_color": "red",
                "estimated_response_time": "Within 24 hours",
                "show_emergency_banner": True,
                "action_card": {
                    "title": "Immediate Action Required",
                    "description": "Consult a lawyer immediately."
                }
            }

        elif severity == "medium":

            recommendation = {
                "priority": "Soon",
                "priority_color": "orange",
                "estimated_response_time": "Within 2-3 days",
                "show_emergency_banner": False,
                "action_card": {
                    "title": "Legal Advice Recommended",
                    "description": "Monitor the situation and prepare your documents."
                }
            }

        ai_response["recommendation"] = recommendation

        return ai_response


recommendation_service = RecommendationService()
