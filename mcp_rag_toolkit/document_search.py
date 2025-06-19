import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

INDEX_PATH = os.path.join(BASE_DIR, "index", "vector.index")
MAPPING_PATH = os.path.join(BASE_DIR, "index", "doc_mapping.pkl")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def search_similar_documents(query: str, top_k: int = 3):
    """
    Search the FAISS index for the top_k documents most similar to the given query.

    Args:
        query (str): User query in natural language.
        top_k (int): Number of top documents to retrieve.

    Returns:
        dict: A dictionary with the query, top_k value, and a list of top matching documents.
              If the index or mapping file is missing, an error message is returned instead.
    """
    if not os.path.exists(INDEX_PATH) or not os.path.exists(MAPPING_PATH):
        return {
            "query": query,
            "top_k": top_k,
            "results": [],
            "error": "Index or document mapping file not found."
        }

    try:
        faiss_index = faiss.read_index(INDEX_PATH)
        with open(MAPPING_PATH, "rb") as f:
            doc_mapping = pickle.load(f)

        embedding = model.encode([query])
        D, I = faiss_index.search(np.array(embedding).astype("float32"), top_k)

        results = []
        for idx in I[0]:
            results.append(doc_mapping.get(idx, f"[Unknown Document #{idx}]"))

        return {
            "query": query,
            "top_k": top_k,
            "results": results
        }

    except Exception as e:
        return {
            "query": query,
            "top_k": top_k,
            "results": [],
            "error": str(e)
        }