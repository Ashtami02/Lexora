import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File

from appp.services.document_analyser import document_analyzer

router = APIRouter()

UPLOAD_FOLDER = "uploads/documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
):

    # ----------------------------------
    # Save Uploaded File
    # ----------------------------------

    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ----------------------------------
    # Analyze Document
    # ----------------------------------

    result = document_analyzer.analyze_document(
        file_path=file_path,
    )

    return result