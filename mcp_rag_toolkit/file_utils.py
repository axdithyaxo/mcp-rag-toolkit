import os
import faiss
import pickle
'''
def list_indexed_files(indexed_files_path: str = None) -> dict:
    try:
        if indexed_files_path is None:
            indexed_files_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index", "doc_mapping.pkl"))
        if not os.path.exists(indexed_files_path):
            return {
                "status": "success",
                "files": []
            }
        with open(indexed_files_path, "rb") as f:
            indexed_data = pickle.load(f)
        
        if isinstance(indexed_data, dict):
            indexed_files = list(indexed_data.keys())
        else:
            indexed_files = indexed_data

        return {
            "status": "success",
            "files": indexed_files
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
'''
def save_indexed_file_paths(file_paths: list, save_path: str = "index/doc_mapping.pkl") -> dict:
    try:
        save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", save_path))
        with open(save_path, "wb") as f:
            pickle.dump(file_paths, f)
        return {"status": "success", "message": f"File paths saved to {save_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# FAISS index save/load helpers
def save_faiss_index(index, index_path: str = "../index/vector.index") -> dict:
    try:
        faiss.write_index(index, index_path)
        return {"status": "success", "message": f"Index saved to {index_path}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def load_faiss_index(index_path: str = "../index/vector.index"):
    try:
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found at {index_path}")
        return faiss.read_index(index_path)
    except Exception as e:
        return {"status": "error", "message": str(e)}
