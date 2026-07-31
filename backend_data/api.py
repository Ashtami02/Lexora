from fastapi import FastAPI
from pydantic import BaseModel

from src.rag_chain import LegalRAG

app = FastAPI(
    title="RGlobe Legal Retrieval API",
    version="2.0.0"
)

# Initialize the retriever
rag = LegalRAG()


class RetrieveRequest(BaseModel):
    question: str
    country: str | None = None
    location: str | None = None
    category: str | None = None
    k: int = 5


@app.get("/")
def home():
    return {
        "message": "RGlobe Legal Retrieval API is running."
    }


@app.post("/retrieve")
def retrieve(request: RetrieveRequest):

    print("\n==============================")
    print("REQUEST RECEIVED")
    print(request)
    print("==============================\n")

    documents = rag.ask(
        question=request.question,
        country=request.country,
        location=request.location,
        category=request.category,
        k=request.k,
    )

    print("TYPE:", type(documents))
    print("DOCUMENTS:")
    print(documents)

    return documents