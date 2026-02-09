import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = "uploads"
VECTOR_DIR = "vectorstore"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
