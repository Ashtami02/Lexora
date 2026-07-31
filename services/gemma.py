import json

from openai import OpenAI

from appp.config import HF_TOKEN


class GemmaService:

    def __init__(self):

        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HF_TOKEN,
        )

        self.model = "google/gemma-4-31B-it:novita"

    # ---------------------------------
    # Normal Generation
    # ---------------------------------

    def generate(
        self,
        prompt: str,
        system_prompt: str = """
You are an expert multilingual AI legal assistant.

Return ONLY valid JSON.

Do NOT wrap the JSON inside markdown.

Do NOT use ```json.

Do NOT explain anything.

Output only the JSON object.
""",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return completion.choices[0].message.content

    # ---------------------------------
    # Streaming Generation
    # ---------------------------------

    def stream_generate(
        self,
        prompt: str,
        system_prompt: str = "You are an expert multilingual AI legal assistant.",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):

        stream = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        for chunk in stream:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta.content

            if delta:
                yield delta

    # ---------------------------------
    # JSON Generation
    # ---------------------------------

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = """
Return ONLY valid JSON.

Do NOT wrap JSON inside markdown.

Do NOT output ```json.

Do NOT explain anything.

Output ONLY the JSON object.
""",
    ):

        response = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )

        try:

            cleaned = response.strip()

            # Remove ```json
            if cleaned.startswith("```json"):
                cleaned = cleaned[len("```json"):]

            # Remove ```
            elif cleaned.startswith("```"):
                cleaned = cleaned[len("```"):]

            # Remove ending ```
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            parsed = json.loads(cleaned)

            print("✅ JSON Parsed Successfully")

            return parsed

        except Exception as e:

            print("\n========================")
            print("JSON Parsing Failed")
            print("========================")
            print(e)
            print("\nRaw Response:\n")
            print(response)
            print("========================\n")

            return {
                "success": False,
                "raw_response": response,
            }

    # ---------------------------------
    # Analyze Case
    # ---------------------------------

    def analyze_case(
        self,
        prompt: str,
    ):
        return self.generate_json(prompt)


gemma_service = GemmaService()