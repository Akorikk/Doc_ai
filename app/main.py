import os
import shutil

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.config import UPLOAD_DIR
from app.utils import parse_document
from app.extraction import extract_fields
from app.guardrails import check_guardrail, confidence_score
from app.rag import (
    process_and_store,
    retrieve,
    generate_answer,
    rewrite_answer,
    load_index
)

# -------- APP INIT --------

app = FastAPI(title="Ultra Doc AI")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------- CHAT MEMORY --------

chat_history = []

# -------- REQUEST MODEL --------

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

# -------- ASK --------

@app.post("/ask")
def ask_question(req: QuestionRequest):

    print(f"User query: {req.question}")  # logging ⭐

    # Retrieve
    try:
        contexts, scores = retrieve(req.question)
    except Exception:
        return {
            "answer": "Please upload a document first.",
            "confidence": 0,
            "sources": []
        }

    # Guardrail
    if not check_guardrail(scores):
        return {
            "answer": "Not found in document.",
            "confidence": 0,
            "sources": []
        }

    # Generate + rewrite
    answer = generate_answer(req.question, contexts)
    answer = rewrite_answer(answer)

    conf = confidence_score(scores[0])

    # Save memory
    chat_history.append({
        "question": req.question,
        "answer": answer
    })

    return {
        "answer": answer,
        "confidence": conf,
        "sources": contexts
    }

# -------- HISTORY --------

@app.get("/history")
def get_history():
    return chat_history

# -------- SUMMARY --------

@app.get("/summary")
def summarize():

    try:
        index, chunks = load_index()
    except:
        return {"summary": "Upload a document first."}

    text = " ".join(chunks[:5])

    return {
        "summary": text[:500]
    }

# -------- EXTRACT --------

@app.post("/extract")
async def extract_doc(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse
    text = parse_document(file_path)

    if not text.strip():
        return {"error": "No text extracted"}

    # Structured extraction
    result = extract_fields(text)

    return result