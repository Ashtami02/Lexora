import requests

from appp.config import RAG_API_URL


class RAGClient:

    def retrieve(
        self,
        question: str,
        country: str,
        location: str,
        category: str,
        k: int = 5,
    ):

        payload = {
            "question": question,
            "country": country,
            "location": location,
            "category": category,
            "k": k,
        }

        try:

            response = requests.post(
                RAG_API_URL,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:

            print(f"RAG Error: {e}")

            return []

    def build_context(self, documents):

        if not documents:

            return "No relevant legal documents were found."

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += f"""

==========================
Document {i}
==========================

Source: {doc.get("source","")}

Country: {doc.get("country","")}

Location: {doc.get("location","")}

Category: {doc.get("category","")}

Page: {doc.get("page","")}

Similarity Score: {doc.get("score","")}

Content:

{doc.get("text","")}

"""

        return context


rag_client = RAGClient()