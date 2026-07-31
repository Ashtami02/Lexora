from src.retriever import LegalRetriever


class LegalRAG:

    def __init__(self):
        self.retriever = LegalRetriever()

    def ask(
        self,
        question: str,
        country: str = None,
        location: str = None,
        category: str = None,
        k: int = 5,
    ):

        docs = self.retriever.retrieve_context(
            question=question,
            country=country,
            location=location,
            category=category,
            k=k,
        )

        # If nothing is found, simply return an empty list
        if not docs:
            return []

        # Return retrieved documents
        return docs