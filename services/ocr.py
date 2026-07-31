import os

import fitz  # PyMuPDF
import easyocr

from docx import Document

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


class OCRService:

    def __init__(self):

        print("OCR Service Initialized.")

        self.readers = {}

        self.language_map = {
            "en": ["en"],
            "hi": ["hi", "en"],
            "bn": ["bn", "en"],
            "ta": ["ta", "en"],
            "te": ["te", "en"],
            "mr": ["mr", "en"],
            "kn": ["kn", "en"],
            "ur": ["ur", "en"],
            "es": ["es", "en"],
            "de": ["de", "en"],
            "fr": ["fr", "en"],
            "pt": ["pt", "en"],
        }

    # ----------------------------------
    # Load EasyOCR Model
    # ----------------------------------

    def get_reader(self, language_code):

        if language_code not in self.language_map:
            language_code = "en"

        if language_code not in self.readers:

            print(f"Loading OCR model: {language_code}")

            self.readers[language_code] = easyocr.Reader(
                self.language_map[language_code],
                gpu=False,
            )

        return self.readers[language_code]

    # ----------------------------------
    # Detect Language
    # ----------------------------------

    def detect_language(self, text):

        try:

            return detect(text)

        except LangDetectException:

            return "en"

    # ----------------------------------
    # PDF Text Extraction
    # ----------------------------------

    def extract_pdf_text(self, file_path):

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text

    # ----------------------------------
    # DOCX Text Extraction
    # ----------------------------------

    def extract_docx_text(self, file_path):

        document = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    # ----------------------------------
    # Image OCR
    # ----------------------------------

    def extract_image_text(self, file_path):

        # First pass in English
        english_reader = self.get_reader("en")

        sample = english_reader.readtext(
            file_path,
            detail=0,
            paragraph=True,
        )

        sample_text = "\n".join(sample)

        language = self.detect_language(sample_text)

        print("Detected Language:", language)

        # Second pass using detected language
        reader = self.get_reader(language)

        result = reader.readtext(
            file_path,
            detail=0,
            paragraph=True,
        )

        text = "\n".join(result)

        return {
            "text": text,
            "language": language,
        }

    # ----------------------------------
    # Main Extraction Function
    # ----------------------------------

    def extract_text(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError("Document not found.")

        extension = os.path.splitext(file_path)[1].lower()

        # -------------------------
        # PDF
        # -------------------------

        if extension == ".pdf":

            text = self.extract_pdf_text(file_path)

            if not text.strip():

                raise Exception(
                    "This appears to be a scanned PDF. OCR support for scanned PDFs will be added next."
                )

            language = self.detect_language(text)

            print("Detected Language:", language)

            return {
                "text": text,
                "language": language,
            }

        # -------------------------
        # DOCX
        # -------------------------

        elif extension == ".docx":

            text = self.extract_docx_text(file_path)

            language = self.detect_language(text)

            print("Detected Language:", language)

            return {
                "text": text,
                "language": language,
            }

        # -------------------------
        # Images (optional)
        # -------------------------

        elif extension in [".jpg", ".jpeg", ".png"]:

            return self.extract_image_text(file_path)

        # -------------------------
        # Unsupported File
        # -------------------------

        else:

            raise Exception(
                f"Unsupported file type: {extension}"
            )


ocr_service = OCRService()