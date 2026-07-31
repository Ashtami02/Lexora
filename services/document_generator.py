from uuid import uuid4

from appp.prompt.doc_gen_prompt import DOCUMENT_GENERATOR_PROMPT
from appp.services.gemma import gemma_service
from appp.generators.pdf_generator import pdf_generator
from appp.generators.docx_generator import docx_generator

class DocumentGenerator:

    def generate(
        self,
        document_type: str,
        country: str,
        state: str,
        language: str,
        description: str,
    ):

        # ----------------------------------
        # Build Prompt
        # ----------------------------------

        prompt = DOCUMENT_GENERATOR_PROMPT.format(
            document_type=document_type,
            country=country,
            state=state,
            language=language,
            description=description,
        )

        # ----------------------------------
        # Generate with Gemma
        # ----------------------------------

        result = gemma_service.generate_json(prompt)
        if "raw_response" in result:
            return {
                "success": False,
                "message": "Gemma returned invalid JSON.",
                "raw_response": result["raw_response"],
            }

        if "title" not in result or "document" not in result:
            return {
                "success": False,
                "message": "Gemma response missing required fields.",
                "response": result,
            }

        title = result["title"]
        document = result["document"]

        # ----------------------------------
        # Extract Response
        # ----------------------------------

        title = result["title"]
        document = result["document"]

        # ----------------------------------
        # Generate Files
        # ----------------------------------

        filename = str(uuid4())

        pdf = pdf_generator.generate(
            output_path=f"generated_documents/{filename}.pdf",
            title=title,
            document_text=document,
        )

        docx = docx_generator.generate(
            output_path=f"generated_documents/{filename}.docx",
            title=title,
            document_text=document,
        )

        # ----------------------------------
        # Attach URLs
        # ----------------------------------

        result["pdf_url"] = pdf["url"]
        result["docx_url"] = docx["url"]
        result["success"] = True

        return result


document_generator = DocumentGenerator()