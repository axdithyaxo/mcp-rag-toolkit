import os
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(__file__)
SAVE_PATH = os.path.join(BASE_DIR, "models", "sbert_model")

def download_model(model_name: str = "all-MiniLM-L6-v2", save_path: str = SAVE_PATH):
    print(f"Downloading model '{model_name}' to '{save_path}'...")
    model = SentenceTransformer(model_name)
    model.save(save_path)
    print("Model downloaded and saved successfully.")

if __name__ == "__main__":
    download_model()