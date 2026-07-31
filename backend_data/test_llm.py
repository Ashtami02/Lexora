from src.vectorstore import VectorStore

db = VectorStore().get_db()

print("Total documents:", db._collection.count())