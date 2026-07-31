from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.config import CHROMA_DIR, EMBEDDING_MODEL


class VectorStore:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.db = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=self.embeddings,
        )

    def get_db(self):

        return self.db