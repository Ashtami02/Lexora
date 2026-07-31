from appp.services.ocr import ocr_service
from appp.services.gemma import gemma_service
from appp.services.pdf_highlighter import pdf_highlighter

from appp.prompt.prompt_builder import PromptBuilder
from appp.prompt.system_prompt import LEGAL_SYSTEM_PROMPT


class DocumentAnalyzer:

    def analyze_document(
        self,
        file_path: str,
    ):

        # ----------------------------------
        # Step 1: OCR
        # ----------------------------------

        ocr_result = ocr_service.extract_text(file_path)

        document_text = ocr_result["text"]

        language_codes = {
            "en": "English",
            "hi": "Hindi",
            "de": "German",
            "es": "Spanish",
            "fr": "French",
            "pt": "Portuguese",
            "ta": "Tamil",
            "bn": "Bengali",
            "te": "Telugu",
            "mr": "Marathi",
            "kn": "Kannada",
            "ur": "Urdu",
        }

        response_language = language_codes.get(
            ocr_result["language"],
            "English",
        )
        if not document_text.strip():

            return {
                "success": False,
                "message": "No text could be extracted from the uploaded document."
            }

        # ----------------------------------
        # Step 2: Build Prompt
        # ----------------------------------

        prompt = PromptBuilder.build_document_analysis_prompt(
        document_text=document_text,
        response_language=response_language,
        )

        # ----------------------------------
        # Step 3: Gemma Analysis
        # ----------------------------------

        result = gemma_service.generate_json(
            prompt=prompt,
            system_prompt=LEGAL_SYSTEM_PROMPT,
        )

        if not isinstance(result, dict):

            return {
                "success": False,
                "message": "Gemma returned an invalid response."
            }

        # ----------------------------------
        # Step 4: Highlight PDF
        # ----------------------------------

    
        highlighted_pdf = None

        if (
            file_path.lower().endswith(".pdf")
            and "annotations" in result
        ):

            print("===== Highlight Debug =====")
            print("PDF Path:", file_path)
            print("Annotations:", result["annotations"])

            try:

                highlighted = pdf_highlighter.highlight_pdf(
                    pdf_path=file_path,
                    annotations=result["annotations"],
                )

                print("Highlight Result:", highlighted)

                highlighted_pdf = highlighted["url"]

            except Exception:

                import traceback

                print("\n===== Highlight Exception =====")
                traceback.print_exc()
                print("===============================\n")

                highlighted_pdf = None

        # ----------------------------------
        # Step 5: Return
        # ----------------------------------

        result["highlighted_pdf"] = highlighted_pdf
        result["success"] = True

        return result


document_analyzer = DocumentAnalyzer()