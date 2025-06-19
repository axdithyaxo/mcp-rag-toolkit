import os
import fitz  # PyMuPDF
from docx import Document

def read_file_content(filepath: str) -> dict:
    try:
        if not os.path.exists(filepath):
            return {
                "status": "error",
                "error_code": "FILE_NOT_FOUND",
                "error_message": f"File not found: {filepath}"
            }

        _, ext = os.path.splitext(filepath)
        ext = ext.lower()
        content = ""

        if ext in ('.txt', '.md', '.html'):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

        elif ext == '.docx':
            doc = Document(filepath)
            content = "\n".join([p.text for p in doc.paragraphs])

        elif ext == '.pdf':
            pdf_doc = fitz.open(filepath)
            content = "\n".join([page.get_text() for page in pdf_doc])

        else:
            return {
                "status": "error",
                "error_code": "UNSUPPORTED_FILE_TYPE",
                "error_message": f"Unsupported file type: {ext}"
            }

        return {
            "status": "success",
            "content": content,
            "content_length": len(content),
            "file_info": {
                "path": filepath,
                "type": ext.lstrip('.'),
                "size": os.path.getsize(filepath),
                "encoding": "utf-8"
            },
            "truncated": False
        }

    except Exception as e:
        return {
            "status": "error",
            "error_code": "EXCEPTION",
            "error_message": str(e)
        }