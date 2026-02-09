import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DIR

model = SentenceTransformer("all-MiniLM-L6-v2")

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

    faiss.write_index(index, f"{VECTOR_DIR}/faiss.index")

    # Save chunks for retrieval
    with open(f"{VECTOR_DIR}/chunks.txt", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(c.replace("\n"," ") + "\n---\n")

    return len(chunks)
