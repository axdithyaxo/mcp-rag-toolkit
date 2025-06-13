import os
import time
import faiss
import pickle
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "enterprise_rag_sample_docs_v3"))
INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index", "faiss.index"))
DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index", "doc_texts.pkl"))

def get_file_metadata(file_path: str) -> dict:
    try:
        abs_path = file_path
        if not os.path.isabs(file_path):
            abs_path = os.path.join(BASE_PATH, file_path)
        stat = os.stat(abs_path)
        ext = os.path.splitext(file_path)[1].lower()
        return {
            "file_type": ext.lstrip("."),
            "last_modified": time.strftime("%Y-%m-%d", time.localtime(stat.st_mtime)),
            "size_bytes": stat.st_size,
        }
    except Exception:
        return {}

def search_documents(question: str, top_k: int = 3) -> dict:
    start_time = time.time()

    if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCS_PATH):
        return {
            "error": "Index files missing. Please run the indexing script first."
        }

    index = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, "rb") as f:
        filepaths = pickle.load(f)

    q_vec = MODEL.encode([question])
    scores, indices = index.search(q_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(filepaths):
            continue
        fp = filepaths[idx]
        meta = get_file_metadata(fp)
        snippet = f"Document: {os.path.basename(fp)}"
        results.append({
            "file_path": fp,
            "content_snippet": snippet,
            "relevance_score": float(score),
            "metadata": meta
        })

    return {
        "documents": results,
        "query": question,
        "total_results": len(results),
        "search_time_ms": int((time.time() - start_time) * 1000)
    }