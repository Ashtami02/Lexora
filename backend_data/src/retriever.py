from typing import Optional

from src.vectorstore import VectorStore
from src.pdf_links import PDF_LINKS

class LegalRetriever:

    def __init__(self):
        self.db = VectorStore().get_db()

    def retrieve_context(
    self,
    question: str,
    country: Optional[str] = None,
    location: Optional[str] = None,
    category: Optional[str] = None,
    k: int = 5,
):

        if country:
            country = country.strip().lower()

        if location:
            location = location.strip().lower()

        if category:
            category = category.strip().lower()

        conditions = []

        if country:
            conditions.append({"country": country})

        if location:
            conditions.append({"location": location})

        if category:
            conditions.append({"category": category})

        # First attempt: filtered search
        if len(conditions) == 0:

            docs = self.db.similarity_search(
                query=question,
                k=k,
            )

        elif len(conditions) == 1:

            docs = self.db.similarity_search(
                query=question,
                k=k,
                filter=conditions[0],
            )

        else:

            docs = self.db.similarity_search(
                query=question,
                k=k,
                filter={
                    "$and": conditions
                },
            )

        # Fallback if no documents found
        if not docs:

            print("No documents found with metadata filters.")
            print("Running semantic fallback search...")

            docs = self.db.similarity_search(
                query=question,
                k=k,
            )

        results = []

        for doc in docs:

            source = doc.metadata.get("source")

            results.append(
                {
                    "text": doc.page_content,
                    "source": source,
                    "page": doc.metadata.get("page"),
                    "country": doc.metadata.get("country"),
                    "location": doc.metadata.get("location"),
                    "category": doc.metadata.get("category"),
                    "pdf_url": PDF_LINKS.get(source),
                }
            )

        print("FINAL DOCUMENT COUNT:", len(results))

        return results