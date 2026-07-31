from pathlib import Path


def extract_metadata(pdf_path: Path) -> dict:
    """
    Extract metadata from the folder structure.

    Expected structure:

    data/
        Country/
            Location/
                Category/
                    file.pdf
    """

    parts = pdf_path.parts

    metadata = {
        "country": "Unknown",
        "location": "Unknown",
        "category": "Unknown",
        "source": pdf_path.name,
        "file_name": pdf_path.stem,
    }

    try:
        data_index = parts.index("data")

        metadata["country"] = parts[data_index + 1].lower()
        metadata["location"] = parts[data_index + 2].replace("_", " ").lower()
        metadata["category"] = parts[data_index + 3].lower()

    except (ValueError, IndexError):
        pass

    return metadata