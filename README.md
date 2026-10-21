# Lexora: AI-Powered Legal Assistance (Backend)

Lexora is a "Legal GPS" for everyday people. A user describes a legal problem in plain language, and Lexora explains their rights, outlines their options, and suggests practical next steps based on their location and the applicable laws.

> **This repository contains the backend only** (Python + FastAPI). The Next.js frontend is maintained separately.

> **Disclaimer:** Lexora provides general legal information, not legal advice. AI-generated guidance can be wrong or incomplete and does not replace a qualified lawyer.

## What it focuses on

Early legal help for common situations where people feel lost:

- Rental disputes and eviction
- Arrest and bail-related issues
- Understanding legal documents and notices

## How it works

```
User question
     |
     v
FastAPI route  -->  Service layer  -->  Retriever (ChromaDB, vector embeddings)
                         |                         |
                         |                 relevant legal passages
                         v                         |
                  Prompt builder  <----------------+
                         |
                         v
                  Google Gemma (LLM)
                         |
                         v
        Explanation, rights, options, next steps
```

1. The user's issue and location arrive through a REST endpoint.
2. The service layer retrieves relevant legal text from a vector store (RAG).
3. A prompt combines the question, the retrieved passages, and jurisdiction context.
4. Google Gemma generates a grounded, plain-language answer.
5. Lawyer search runs separately against a SQLite database.

## Features and status

| Feature | Status |
|---|---|
| AI Legal Advisor (Gemma + RAG, jurisdiction-aware) | Implemented |
| Legal Document Generator (structured documents and notices) | Implemented |
| Find a Lawyer (by specialization and location, SQLite) | Implemented |
| Legal Document Analyzer (clauses, risks, recommendations) | Planned |
| Legal Timeline Generator | Planned |
| Court Rehearsal simulation | Planned |
| Multilingual assistance | Planned |

## Tech stack

| Layer | Technology |
|---|---|
| API | Python, FastAPI |
| LLM | Google Gemma |
| Retrieval | RAG, vector embeddings, ChromaDB |
| Database | SQLite (lawyer directory) |
| Architecture | REST APIs between frontend, AI services, and retrieval |

## Project structure

```
Lexora/
├── main.py            FastAPI app entry point
├── config.py          settings and configuration
├── routes/            API endpoints
├── schemas/           request and response models
├── services/          business logic: retrieval, LLM calls
├── prompt/            prompt templates
├── generators/        legal document generation
├── database/          database setup and access
├── lawyer_database/   lawyer directory data
└── backend_data/      legal source data used for retrieval
```

## Running locally

```bash
git clone https://github.com/Ashtami02/Lexora.git
cd Lexora
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Interactive API docs are available at `http://localhost:8000/docs`.

Set any required keys or model settings in `config.py` or your environment before running. Do not commit secrets.

## Limitations

- Answers are only as good as the legal sources loaded into the vector store.
- Coverage is limited to the topics and jurisdictions in the loaded data.
- Several planned features are not built yet (see the status table above).
- This is a student project and has not been reviewed by legal professionals.

## Author

Built by [Ashtami Choudhary](https://github.com/Ashtami02) (backend).
