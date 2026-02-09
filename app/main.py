import os
import shutil
from fastapi import FastAPI, UploadFile, File

from app.utils import parse_document
from app.rag import process_and_store
from app.config import UPLOAD_DIR

app = FastAPI()

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_document(file_path)

    if not text.strip():
        return {"error": "No text extracted"}

    num_chunks = process_and_store(text)

    return {
        "message": "Uploaded & processed",
        "chunks_created": num_chunks
    }
