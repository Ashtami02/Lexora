from pathlib import Path
import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.loader import PDFLoader
from src.config import CHROMA_DIR, EMBEDDING_MODEL
# ----------------------------
# Delete old database
# ----------------------------

if CHROMA_DIR.exists():
    shutil.rmtree(CHROMA_DIR)

# ----------------------------
# Load documents
# ----------------------------

loader = PDFLoader()

documents = loader.load_documents()

# ----------------------------
# Split documents
# ----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.\n")

# ----------------------------
# Embedding Model
# ----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

# ----------------------------
# Create Chroma DB
# ----------------------------

db = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings,
)

# ----------------------------
# Insert in batches
# ----------------------------

BATCH_SIZE = 25

for i in range(0, len(chunks), BATCH_SIZE):

    batch = chunks[i : i + BATCH_SIZE]

    print(
        f"Adding batch {i // BATCH_SIZE + 1}/"
        f"{(len(chunks) - 1) // BATCH_SIZE + 1}"
    )

    db.add_documents(batch)

print("\n✅ Chroma database created successfully!")