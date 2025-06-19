# ZenithTech RAG Toolkit

**ZenithTech RAG Toolkit** is a fully local, production-ready Retrieval-Augmented Generation (RAG) system built using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), FAISS, Sentence Transformers, and PostgreSQL. It allows you to semantically search both unstructured documents and structured data and respond intelligently to natural language queries.

---

## 🌟 Features

- 🔍 **Semantic Search** over local documents using FAISS and Sentence Transformers
- 🧠 **LLM-augmented Prompt Generation** with context-aware answer generation
- 🗃️ **Support for structured (SQL)** and **unstructured (PDF, DOCX, TXT, etc.)** data
- ⚙️ **Agentic Tool Design** using FastMCP and Claude Desktop
- 📦 Modular tool structure for easy extension and maintainability
- 🕒 **Auto-updating** FAISS index using cron jobs
- 🔐 Fully local and private — no external APIs needed

---

## 📁 Project Structure

```
mcp-rag-toolkit/
├── data/                         # Sample documents
├── index/                        # Saved FAISS index + doc mapping
├── auto_updates/                # Cron scripts for periodic indexing
├── mcp_rag_toolkit/
│   ├── server.py                 # Main MCP server
│   ├── read_utils.py            # File readers
│   ├── query_executor.py        # SQL query handler
│   ├── index_document_tool.py   # Index documents into FAISS
│   ├── document_search.py       # Semantic similarity search
│   ├── file_utils.py            # Save/load helpers for FAISS + mapping
│   ├── model_downloader.py      # Downloads SBERT model
```

> 📂 To use your own data, add your company’s structured and unstructured documents inside the `data/` directory (e.g., `data/my_company_docs/`). The system will automatically index and retrieve from this location during search.

---

## 🚀 How It Works

### 🔧 Tools Implemented

| Tool Name             | Description                                                |
|----------------------|------------------------------------------------------------|
| `read_file`          | Reads content from a document                             |
| `query_sql`          | Executes a SQL query on a local PostgreSQL DB             |
| `semantic_search`    | Returns top-k documents by semantic similarity            |
| `index_document`     | Indexes documents using SentenceTransformers + FAISS      |
| `list_indexed_files` | (Optional) Lists paths of indexed files                   |
| `rag_prompt`         | Dynamically generates a contextual LLM prompt             |

### 🧠 Prompting Flow

- User asks a question
- `rag_prompt` → `semantic_search` → top-k docs
- Each document is read via `read_file`
- A structured context block is added to the final prompt
- Claude or other MCP-compatible clients generate the final answer

---

## 📦 Setup

### Requirements

- Python 3.10+
- Poetry
- FAISS (CPU)
- PostgreSQL (for SQL-based RAG)

### Installation

```bash
git clone https://github.com/yourusername/mcp-rag-toolkit.git
cd mcp-rag-toolkit
poetry install
poetry shell
```

> 💡 Note: The embedding model will be downloaded on first use via `model_downloader.py`. You can manually trigger it with:
> 
> ```bash
> python mcp_rag_toolkit/model_downloader.py
> ```

---

## 🧪 Usage

### 1. Index Documents

```bash
python mcp_rag_toolkit/index_document_tool.py
```

### 2. Start the MCP Server

```bash
mcp run mcp_rag_toolkit/server.py
```

### 3. Interact via Claude Desktop or MCP Inspector

Try asking:

```
"What are the minimum system requirements for ZenithTech software on Ubuntu?"
```

or

```
"Summarize the Q3 finance meeting notes."
```

---

## 🛠️ Cron-based Auto Reindexing

To keep the document index fresh, use:

```bash
crontab auto_updates/crontab_example.txt
```

This will periodically reindex documents via `update_index_tool.py`.

---

## 🧠 Models

- **Embedding Model**: [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

> 📦 To reduce repository size, the model weights are not bundled by default. Ensure `model_downloader.py` has run to populate `mcp_rag_toolkit/models/`.

- FAISS index: stored at `index/vector.index`
- Mapping file: `index/doc_mapping.pkl`

---

## 📜 License

MIT License © 2025 Aadithya Vishnu Sajeev

---

## 🙌 Acknowledgements

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FAISS by Facebook](https://github.com/facebookresearch/faiss)
- [SentenceTransformers](https://www.sbert.net/)
- Claude AI / Anthropic for Desktop Agent Integration
