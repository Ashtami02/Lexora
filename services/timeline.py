from appp.prompt.timeline_prompt import (
    TIMELINE_PROMPT
)

from appp.services.gemma import (
    gemma_service
)


class TimelineService:

    def generate_timeline(
        self,
        issue: str,
        country: str,
        state: str,
        recommended_option: str,
        recommendation_reason: str = "",
        required_documents=None,
        next_steps=None,
        action_plan=None,
    ):

        # ----------------------------------
        # Handle Empty Values
        # ----------------------------------

        required_documents = (
            required_documents or []
        )

        next_steps = (
            next_steps or []
        )

        action_plan = (
            action_plan or []
        )

        # ----------------------------------
        # Build Prompt
        # ----------------------------------

        prompt = TIMELINE_PROMPT.format(

            issue=issue,

            country=country,

            state=state,

            recommended_option=
                recommended_option,

            recommendation_reason=
                recommendation_reason,

            required_documents=
                required_documents,

            next_steps=
                next_steps,

            action_plan=
                action_plan,

        )

        # ----------------------------------
        # Generate Timeline Using Gemma
        # ----------------------------------

        result = gemma_service.generate_json(
            prompt
        )

        # ----------------------------------
        # Handle Invalid JSON
        # ----------------------------------

        if "raw_response" in result:

            return {

                "success": False,

                "message":
                    "Gemma returned invalid JSON.",

                "raw_response":
                    result["raw_response"],

            }

        # ----------------------------------
        # Return Timeline
        # ----------------------------------

        return {

            "success": True,

            "current_status":
                result.get(
                    "current_status",
                    ""
                ),

            "estimated_completion":
                result.get(
                    "estimated_completion",
                    ""
                ),

            "next_step":
                result.get(
                    "next_step",
                    ""
                ),

            "timeline":
                result.get(
                    "timeline",
                    []
                ),

        }


timeline_service = TimelineService()