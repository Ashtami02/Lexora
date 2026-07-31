from src.embeddings import EmbeddingModel


class DocumentEmbedder:

    def __init__(self):

        self.embedding_model = EmbeddingModel().get_embedding_model()

    def embed_documents(self, chunks):

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        return embeddings
    