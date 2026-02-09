import os
import shutil

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.extraction import extract_fields
from app.utils import parse_document
from app.rag import process_and_store, retrieve, generate_answer
from app.guardrails import check_guardrail, confidence_score
from app.config import UPLOAD_DIR

# -------- APP INIT --------

app = FastAPI(title="Ultra Doc AI")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------- REQUEST MODELS --------

class QuestionRequest(BaseModel):
    question: str

# -------- ROOT --------

@app.get("/")
def home():
    return {"message": "Ultra Doc AI is running 🚀"}

# -------- UPLOAD --------

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse text
    text = parse_document(file_path)

    if not text.strip():
        return {"error": "No text extracted from document"}

    # Create embeddings + store
    num_chunks = process_and_store(text)

    return {
        "message": "Uploaded & processed successfully",
        "chunks_created": num_chunks
    }

# -------- ASK (RAG Q&A) --------

@app.post("/ask")
def ask_question(req: QuestionRequest):

    # Safety: index exists?
    try:
        contexts, scores = retrieve(req.question)
    except Exception:
        return {
            "answer": "Please upload a document first",
            "confidence": 0,
            "sources": []
        }

    # Guardrail
    if not check_guardrail(scores):
        return {
            "answer": "Not found in document",
            "confidence": 0,
            "sources": []
        }

    # Generate answer
    answer = generate_answer(req.question, contexts)

    conf = confidence_score(scores[0])

    return {
        "answer": answer,
        "confidence": conf,
        "sources": contexts
    }

# -------- EXTRACT (Structured Data) --------

@app.post("/extract")
async def extract_doc(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse text
    text = parse_document(file_path)

    if not text.strip():
        return {"error": "No text extracted"}

    # Extract structured fields
    result = extract_fields(text)

    return result