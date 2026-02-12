from pypdf import PdfReader
import docx
import re

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def parse_document(file_path: str) -> str:
    text = ""

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    return clean_text(text)
