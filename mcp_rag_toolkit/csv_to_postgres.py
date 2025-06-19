## 📂 Customizing Your Data and Model

To use this RAG toolkit with your own enterprise data:

1. **Add Your Company Documents**:
   - Place your structured and unstructured files inside the `data/` folder following the sample directory structure (e.g., `data/enterprise_rag_sample_docs_v3/hr/`, `finance/`, `it/`, etc.).
   - Supported file types include `.txt`, `.md`, `.csv`, `.html`, `.docx`, and `.pdf`.

2. **Use Your Own Embedding Model** (Optional):
   - By default, this project uses the `all-MiniLM-L6-v2` SentenceTransformer model.
   - If you'd like to use your own pre-trained or fine-tuned embedding model:
     - Download the model and update the `index_document_tool.py` and `document_search.py` to load from your local path or model repo.
     - Ensure compatibility with SentenceTransformers and FAISS indexing.
