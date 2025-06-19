import os
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss

from mcp_rag_toolkit.file_utils import save_faiss_index

DATA_DIR = os.path.abspath("data/enterprise_rag_sample_docs_v3")
INDEX_DIR = os.path.abspath("index")
INDEX_PATH = os.path.join(INDEX_DIR, "vector.index")
MAPPING_PATH = os.path.join(INDEX_DIR, "doc_mapping.pkl")
MODEL_PATH = os.path.abspath("mcp_rag_toolkit/models/sbert_model")

# Ensure index directory exists
os.makedirs(INDEX_DIR, exist_ok=True)

# Load existing mapping if available
indexed_files = {}
if os.path.exists(MAPPING_PATH):
    try:
        with open(MAPPING_PATH, "rb") as f:
            loaded = pickle.load(f)
            if isinstance(loaded, dict):
                indexed_files = loaded
            elif isinstance(loaded, list):
                # Convert old list to dict and save
                indexed_files = {path: True for path in loaded}
                with open(MAPPING_PATH, "wb") as wf:
                    pickle.dump(indexed_files, wf)
            else:
                print("⚠️ Unrecognized mapping format, resetting.")
    except Exception as e:
        print(f"⚠️ Failed to load mapping file: {e}")

# Ensure MAPPING_PATH always contains updated dict after indexing
...
# After adding new entries:
# Save updated mapping
with open(MAPPING_PATH, "wb") as f:
    pickle.dump(indexed_files, f)
# Initialize model
model = SentenceTransformer(MODEL_PATH)

documents = []
file_paths = []

# Walk through the data directory
for root, _, files in os.walk(DATA_DIR):
    for file in files:
        ext = file.lower().split(".")[-1]
        if ext in ["txt", "md", "html", "pdf", "docx"]:
            file_path = os.path.join(root, file)
            if file_path not in indexed_files:
                try:
                    content = ""
                    if ext in ["txt", "md", "html"]:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                    elif ext == "pdf":
                        import fitz
                        with fitz.open(file_path) as pdf_doc:
                            content = "\n".join(page.get_text() for page in pdf_doc)
                    elif ext == "docx":
                        from docx import Document
                        doc = Document(file_path)
                        content = "\n".join(para.text for para in doc.paragraphs)

                    if content.strip():
                        documents.append(content)
                        file_paths.append(file_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# If no new documents, exit early
if not documents:
    print("No new documents to index.")
    exit()

# Encode documents
embeddings = model.encode(documents)

# Load or create FAISS index
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)

index.add(embeddings)

# Update mapping
for path in file_paths:
    indexed_files[path] = True

# Save index and mapping
save_faiss_index(index, INDEX_PATH)
with open(MAPPING_PATH, "wb") as f:
    pickle.dump(indexed_files, f)

print(f"Indexed {len(documents)} new documents into {INDEX_PATH}")
