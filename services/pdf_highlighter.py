import os
import fitz  # PyMuPDF


HIGHLIGHTED_FOLDER = "uploads/highlighted"
os.makedirs(HIGHLIGHTED_FOLDER, exist_ok=True)


class PDFHighlighter:

    def highlight_pdf(
        self,
        pdf_path: str,
        annotations: list,
    ):

        # -----------------------------
        # Open PDF
        # -----------------------------

        doc = fitz.open(pdf_path)

        # -----------------------------
        # Highlight annotations
        # -----------------------------

        for annotation in annotations:

            text = annotation.get("text", "").strip()

            if not text:
                continue

            severity = annotation.get(
                "severity",
                "Medium"
            ).lower()

            reason = annotation.get(
                "reason",
                ""
            )

            annotation_type = annotation.get(
                "type",
                ""
            )

            # Search every page

            for page in doc:

                matches = page.search_for(text)

                if not matches:
                    continue

                for rect in matches:

                    highlight = page.add_highlight_annot(rect)

                    # -------------------------
                    # Highlight Colors
                    # -------------------------

                    if severity == "critical":

                        # Red
                        highlight.set_colors(stroke=(1, 0, 0))

                    elif severity == "high":

                        # Orange
                        highlight.set_colors(stroke=(1, 0.5, 0))

                    elif severity == "medium":

                        # Yellow
                        highlight.set_colors(stroke=(1, 1, 0))

                    else:

                        # Green
                        highlight.set_colors(stroke=(0, 1, 0))

                    # -------------------------
                    # Popup Comment
                    # -------------------------

                    highlight.set_info(
                        content=f"""
Type: {annotation_type}

Severity: {severity.title()}

Reason:
{reason}
"""
                    )

                    highlight.update()

        # -----------------------------
        # Save PDF
        # -----------------------------

        filename = os.path.basename(pdf_path)

        filename = filename.replace(
            ".pdf",
            "_highlighted.pdf",
        )

        output_path = os.path.join(
            HIGHLIGHTED_FOLDER,
            filename,
        )

        doc.save(
            output_path,
            garbage=4,
            deflate=True,
        )

        doc.close()

        # -----------------------------
        # Return Download URL
        # -----------------------------

        return {
            "path": output_path,
            "url": f"/downloads/{filename}",
        }


pdf_highlighter = PDFHighlighter()