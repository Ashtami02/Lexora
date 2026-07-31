from fastapi import FastAPI

from appp.routes.analyse import router as analyze_router
from fastapi.staticfiles import StaticFiles
from appp.routes.documents import router as document_router
from appp.routes.court import router as court_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Legal Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)


@app.get("/")
def home():
    return {
        "message": "AI Legal Assistant Backend Running"
    }
    
    
from appp.routes.legal import router as legal_router

app.include_router(
    legal_router,
    prefix="/legal-advisor",
    tags=["Legal Advisor"],
)

app.include_router(
    document_router,
    prefix="/document-analyzer",
    tags=["Document Analyzer"],
)

app.mount(
    "/downloads",
    StaticFiles(directory="uploads/highlighted"),
    name="downloads",
)

from appp.routes.doc_gen import router as document_generator_router

app.include_router(
    document_generator_router,
    prefix="/document-generator",
    tags=["Document Generator"],
)


from fastapi.staticfiles import StaticFiles

import os

os.makedirs("generated_documents", exist_ok=True)
app.mount(
    "/generated_documents",
    StaticFiles(directory="generated_documents"),
    name="generated_documents",
)

app.include_router(
    court_router,
    prefix="/court",
    tags=["Court Rehearsal"],
)

from appp.routes.timeline import router as timeline_router

app.include_router(
    timeline_router
)