import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "..", "index", "faiss.index")
DOCS_PATH = os.path.join(BASE_DIR, "..", "index", "doc_texts.pkl")

def search_documents(question: str, top_k: int = 3) -> str:
    if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCS_PATH):
        return "⚠️ FAISS index or doc_texts.pkl not found. Please run `setup_data.py` from the root project directory."
    
    index = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, "rb") as f:
        filepaths = pickle.load(f)

    q_vec = MODEL.encode([question])
    _, indices = index.search(q_vec, top_k)

    return {
    "results": [
        {"rank": i + 1, "path": filepaths[idx]}
        for i, idx in enumerate(indices[0])
    ]
}