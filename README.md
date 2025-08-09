# ZenithTech RAG Toolkit

**ZenithTech RAG Toolkit** is a fully local, production-ready Retrieval-Augmented Generation (RAG) system built using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), FAISS, Sentence Transformers, and PostgreSQL.

It enables semantic search over both structured (SQL) and unstructured (PDF, DOCX, TXT, CSV, HTML, etc.) company documents, and can integrate directly with Claude Desktop or any MCP-compatible client to answer natural language queries with context-aware responses — all without sending data to external APIs.

---

## Key Features

- Semantic Search — FAISS + Sentence Transformers for top-k similarity search on your local documents.
- Context-Aware Answer Generation — Automatically retrieves and injects relevant document context into LLM prompts.
- Supports Structured & Unstructured Data — Works with SQL databases and file formats like PDF, DOCX, TXT, CSV, HTML.
- Agentic Tool Design — Each capability is an independent MCP tool for modularity and extensibility.
- Automatic Document Indexing — Update your FAISS index on a schedule using cron jobs.
- Fully Local & Private — No external API calls; all data stays on your machine.

---

mcp-rag-toolkit/
├── data/                         # Place your company documents here
├── index/                        # FAISS index + document mapping
├── auto_updates/                 # Cron jobs for periodic re-indexing
├── mcp_rag_toolkit/
│   ├── server.py                  # MCP server entrypoint
│   ├── index_document_tool.py     # Indexes all supported docs in /data
│   ├── document_search.py         # Semantic search logic
│   ├── read_utils.py              # File reading utilities
│   ├── query_executor.py          # SQL query execution
│   ├── file_utils.py              # Save/load helpers for index & mapping
│   ├── model_downloader.py        # Downloads SBERT model if missing
│   ├── update_index_tool.py       # Refreshes FAISS index

To use your own company data, add all structured and unstructured files to the `data/` directory before indexing.  
> Example:  
> ```
> data/my_company_docs/
>    ├── hr_policies.pdf
>    ├── Q1_financial_report.xlsx
>    ├── meeting_notes.docx
> ```

---

## How It Works

### Tool Overview

| Tool Name          | Purpose |
|-------------------|---------|
| `semantic_search` | Finds top-k most relevant documents based on user query. |
| `read_file`       | Reads and returns file content. |
| `query_sql`       | Executes SQL queries against PostgreSQL DB. |
| `index_document`  | Builds FAISS index from local documents. |
| `rag_prompt`      | Combines semantic search + document reading to generate context-rich prompts for the LLM. |

### Processing Flow

1. User sends a natural language query.
2. `rag_prompt` triggers:
   - `semantic_search` → Retrieves top-k relevant documents.
   - `read_file` → Loads full content of each relevant document.
3. The retrieved content is injected into the final LLM prompt.
4. MCP client (e.g., Claude Desktop) generates a context-aware answer.

---

## Setup Instructions

### 1. Requirements
- Python 3.10+
- [Poetry](https://python-poetry.org/) (for dependency management)
- FAISS (CPU version)
- PostgreSQL (optional, for SQL data search)

### 2. Installation

```bash
# Clone the repository
git clone git@github.com:yourusername/mcp-rag-toolkit.git
cd mcp-rag-toolkit

# Install dependencies
poetry install
poetry shell

# Download the SBERT model (optional step)
python mcp_rag_toolkit/model_downloader.py

Usage

1. Add Your Company Data

Place all files you want searchable into the data/ directory. Supported formats:
PDF, DOCX, TXT, CSV, HTML, Markdown, JSON

2. Index Documents

python mcp_rag_toolkit/index_document_tool.py

3. Start the MCP Server

mcp run mcp_rag_toolkit/server.py

Example queries:
"What are the onboarding steps in our HR policies?"
"Summarize the Q3 financial report."

Automatic Index Updates

This toolkit supports scheduled auto indexing so new or modified files in the data/ directory are automatically picked up without manual indexing.

How It Works
	•	A cron job periodically runs update_index_tool.py
	•	The script checks for new or updated files
	•	FAISS index and mapping file are updated accordingly

Setup Example (Mac/Linux)

Edit your crontab:
crontab -e

Add an entry to run indexing every day at midnight:
0 0 * * * /path/to/poetry run python /path/to/mcp-rag-toolkit/mcp_rag_toolkit/update_index_tool.py >> /path/to/mcp-rag-toolkit/auto_updates/cron_debug.log 2>&1

Or use the provided example:
crontab auto_updates/crontab_example.txt

Models & Storage
	•	Embedding Model: sentence-transformers/all-MiniLM-L6-v2
	•	FAISS Index: index/vector.index
	•	Document Mapping: index/doc_mapping.pkl

Model files are downloaded on first run and stored in:
mcp_rag_toolkit/models/

Privacy & Security
	•	All processing happens locally — no data leaves your machine.
	•	Suitable for sensitive enterprise environments.

License

MIT License © 2025 Aadithya Vishnu Sajeev

Acknowledgements
	•	Model Context Protocol
	•	FAISS
	•	SentenceTransformers
	•	Claude AI / Anthropic
