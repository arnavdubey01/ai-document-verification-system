from google.api_core.client_options import ClientOptions
from google.cloud import documentai

PROJECT_ID = "ai-document-verification"
LOCATION = "asia-south1"
PROCESSOR_ID = "dff967f12d3a70f0"

def extract_text_with_document_ai(file_path, mime_type):
    opts = ClientOptions(
        api_endpoint=f"{LOCATION}-documentai.googleapis.com"
    )

    client = documentai.DocumentProcessorServiceClient(
        client_options=opts
    )

    processor_name = client.processor_path(
        PROJECT_ID,
        LOCATION,
        PROCESSOR_ID
    )

    with open(file_path, "rb") as file:
        file_content = file.read()

    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type
    )

    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document
    )

    result = client.process_document(request=request)

    return result.document.text