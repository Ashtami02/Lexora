from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from src.utils import get_pdf_files
from src.config import DATA_DIR
from src.metadata import extract_metadata

class PDFLoader:

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir

    def load_documents(self):

        documents = []

        pdf_files = get_pdf_files(self.data_dir)

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found inside {self.data_dir}"
            )

        print(f"Found {len(pdf_files)} PDF(s)\n")

        for pdf in pdf_files:

            print(f"Loading {pdf.name}")

            loader = PyPDFLoader(str(pdf))

            pdf_docs = loader.load()

            # Add custom metadata
            metadata = extract_metadata(pdf)

            for doc in pdf_docs:

                # Keep the page number added by PyPDFLoader
                doc.metadata.update(metadata)

            documents.extend(pdf_docs)

        print(f"\nLoaded {len(documents)} pages.\n")

        return documents