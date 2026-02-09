import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DIR

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- PROCESS & STORE --------

def process_and_store(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_text(text)

    embeddings = model.encode(chunks)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    os.makedirs(VECTOR_DIR, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, f"{VECTOR_DIR}/faiss.index")

    # Save chunks
    with open(f"{VECTOR_DIR}/chunks.txt", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(c.replace("\n", " ") + "\n---\n")

    return len(chunks)

# -------- LOAD INDEX --------

def load_index():

    index_path = f"{VECTOR_DIR}/faiss.index"
    chunk_path = f"{VECTOR_DIR}/chunks.txt"

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        raise ValueError("No document uploaded")

    index = faiss.read_index(index_path)

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = f.read().split("\n---\n")

    return index, chunks

# -------- RETRIEVE --------

def retrieve(query, k=3):

    index, chunks = load_index()

    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k)

    results = [chunks[i] for i in I[0]]
    scores = [float(s) for s in D[0]]

    return results, scores

# -------- ANSWER --------

def generate_answer(query, contexts):

    context_text = "\n".join(contexts)

    return f"Based on the document:\n{context_text[:500]}"
