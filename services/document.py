from typing import Any

def create_document_data(
        filename: str,
        content_type: str,
        extracted_text: str
) -> dict[str, Any]:

    return {
        "filename": filename,
        "content_type": content_type,
        "raw_text": extracted_text,
        "document_type": None,
        "fields": {},
        "confidence": {},
        "warnings": []
    }