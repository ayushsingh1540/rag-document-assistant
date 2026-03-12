import os
from docx import Document
from pypdf import PdfReader

class DocumentLoader:

    def load_documents(self):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        docs_path = os.path.join(base_dir, "data", "raw_docs")

        print("Reading documents from:", docs_path)

        for root, _, files in os.walk(docs_path):
            for file in files:

                path = os.path.join(root, file)

                if file.endswith(".txt"):
                    with open(path, "r", encoding="utf-8") as f:
                        yield {"doc_id": file, "content": f.read()}

                elif file.endswith(".docx"):
                    doc = Document(path)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    yield {"doc_id": file, "content": text}

                elif file.endswith(".pdf"):
                    reader = PdfReader(path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    yield {"doc_id": file, "content": text}