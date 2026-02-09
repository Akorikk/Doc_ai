from pypdf import PdfReader
import docx

def parse_document(file_path: str) -> str:
    text = ""

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    return text
