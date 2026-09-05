from fastapi import FastAPI, UploadFile, File, HTTPException

from pathlib import Path
from uuid import uuid4

from services.ocr import extract_text_from_image, extract_text_from_pdf


# Folders where uploaded files will be stored:

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed file types:
ALLOWED_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

# Maximum file size:
MAX_FILE_SIZE = 10*1024*1024    # 10 MB



app = FastAPI()

@app.get("/")
def home():
    return {"message": "SIH26188 backend is running."}

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    # Check file type:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, and PNG files are allowed."
        )

    # Read the uploaded file:
    contents = await file.read()

    # Check file size:
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=("File is too large. Max size: 10 MB.")
        )

    # Generate file name (unique)
    extension = ALLOWED_TYPES[file.content_type]
    stored_filename = f"{uuid4()}{extension}"

    # Create complete path
    stored_path = UPLOAD_DIR / stored_filename

    # Save the file
    stored_path.write_bytes(contents)

    # OCR for image:
    print("filename: ", file.filename)
    print("content_type: ", file.content_type)

    extracted_text = None

    if file.content_type in ["image/jpeg", "image/png"]:
        extracted_text = extract_text_from_image(stored_path)

    elif file.content_type == "application/pdf":
        extracted_text = extract_text_from_pdf(stored_path)

    # Send response
    return {
        "message": "FILE uploaded successfully",
        "orginal_filename": file.filename,
        "stored_filename": stored_filename,
        "content_type": file.content_type,
        "size": len(contents),
        # "filename": file.filename,
        # "content_type": file.content_type,
        "extracted_text": extracted_text
    }