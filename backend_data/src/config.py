from pathlib import Path
import os
from dotenv import load_dotenv

# ===========================
# PROJECT PATHS
# ===========================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(dotenv_path=BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# ===========================
# EMBEDDINGS
# ===========================

EMBEDDING_MODEL = "BAAI/bge-m3"

# ===========================
# TEXT SPLITTING
# ===========================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# ===========================
# LLM
# ===========================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


LLM_MODEL = "gemma-4-26b-a4b-it"

# ===========================
# DATABASE
# ===========================

BATCH_SIZE = 25
TOP_K = 5