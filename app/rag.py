import os
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DIR

# ---------------- LOAD EMBEDDING MODEL ----------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- PROCESS & STORE ----------------

def process_and_store(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_text(text)

    embeddings = model.encode(chunks, show_progress_bar=False)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    os.makedirs(VECTOR_DIR, exist_ok=True)

    # Save FAISS index
    faiss.write_index(index, f"{VECTOR_DIR}/faiss.index")

    # Save chunks
    with open(f"{VECTOR_DIR}/chunks.txt", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(c.replace("\n", " ") + "\n---\n")

    return len(chunks)

# ---------------- LOAD INDEX ----------------

def load_index():

    index_path = f"{VECTOR_DIR}/faiss.index"
    chunk_path = f"{VECTOR_DIR}/chunks.txt"

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        raise ValueError("Vector store not found")

    index = faiss.read_index(index_path)

    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = f.read().split("\n---\n")

    return index, chunks

# ---------------- RETRIEVE ----------------

def retrieve(query: str, k: int = 3):

    index, chunks = load_index()

    q_emb = model.encode([query], show_progress_bar=False)
    D, I = index.search(np.array(q_emb).astype("float32"), k)

    results = [chunks[i] for i in I[0] if i < len(chunks)]
    scores = [float(s) for s in D[0]]

    return results, scores

# ---------------- GENERATE ANSWER ----------------

def generate_answer(query: str, contexts: list[str]) -> str:
    """
    Simple extractive answer generator.
    Returns the most relevant sentence instead of dumping text.
    """

    if not contexts:
        return "Not found in document"

    context = contexts[0]

    # Split into sentences
    sentences = context.split(".")

    # Pick first meaningful sentence
    for s in sentences:
        s = s.strip()
        if len(s) > 20:
            return s + "."

    return context[:200] + "..."