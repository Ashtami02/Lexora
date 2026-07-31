import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def generate(
        self,
        output_path: str,
        title: str,
        document_text: str,
    ):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True,
        )

        styles = getSampleStyleSheet()

        pdf = SimpleDocTemplate(output_path)

        story = [

            Paragraph(
                f"<b>{title}</b>",
                styles["Heading1"],
            ),

            Paragraph(
                document_text.replace("\n", "<br/>"),
                styles["BodyText"],
            ),
        ]

        pdf.build(story)

        filename = os.path.basename(output_path)

        return {
            "path": output_path,
            "url": f"/generated_documents/{filename}",
        }


pdf_generator = PDFGenerator()