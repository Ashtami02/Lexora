import os
import torch
from dotenv import load_dotenv

load_dotenv()

# =====================================
# Gemma Configuration
# =====================================


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MAX_NEW_TOKENS = 1024

TEMPERATURE = 0.2

TOP_P = 0.9

DO_SAMPLE = False

# =====================================
# RAG Configuration
# =====================================

TOP_K = 5

# =====================================
# Chat Configuration
# =====================================

MAX_CHAT_HISTORY = 10

# =====================================
# API
# =====================================

API_TITLE = "Lexora"

API_VERSION = "1.0.0"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./lexora.db"
)


import os

from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

RAG_API_URL = "http://localhost:8001/retrieve"

