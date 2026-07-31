from pathlib import Path

def get_pdf_files(folder: Path):
    return list(folder.rglob("*.pdf"))