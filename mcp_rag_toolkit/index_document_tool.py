import os
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from docx import Document
import fitz  # PyMuPDF

from mcp_rag_toolkit.file_utils import save_faiss_index

# Paths
DATA_DIR = "data/enterprise_rag_sample_docs_v3"
INDEX_DIR = "index"
INDEX_FILE = os.path.join(INDEX_DIR, "vector.index")
MAPPING_FILE = os.path.join(INDEX_DIR, "doc_mapping.pkl")

# Load model
model_path = os.path.join("mcp_rag_toolkit", "models", "sbert_model")
model = SentenceTransformer(model_path)

# Collect documents
documents = []
file_paths = []

for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        ext = file.lower()
        if ext.endswith((".txt", ".md", ".html", ".pdf", ".docx")):
            file_path = os.path.join(root, file)
            try:
                content = ""
                if ext.endswith((".txt", ".md", ".html")):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                elif ext.endswith(".docx"):
                    doc = Document(file_path)
                    content = "\n".join([para.text for para in doc.paragraphs])
                elif ext.endswith(".pdf"):
                    pdf_doc = fitz.open(file_path)
                    content = "\n".join([page.get_text() for page in pdf_doc])
                if content.strip():
                    documents.append(content)
                    file_paths.append(file_path)
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

print(f"Found {len(file_paths)} supported documents for indexing.")

# Encode documents
if documents:
    embeddings = model.encode(documents, show_progress_bar=True)

    # Create FAISS index
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and mapping
    os.makedirs(INDEX_DIR, exist_ok=True)
    save_faiss_index(index, INDEX_FILE)
    index_mapping = {i: os.path.abspath(path) for i, path in enumerate(file_paths)}
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(index_mapping, f)

    print(f"Indexed {len(documents)} documents into {INDEX_FILE}")
else:
    print("No documents found to index.")
