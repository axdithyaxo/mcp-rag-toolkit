# ZenithTech RAG Toolkit

**ZenithTech RAG Toolkit** is a fully local, production-ready Retrieval‑Augmented Generation (RAG) system built with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), FAISS, Sentence Transformers, and PostgreSQL.

It enables semantic search over both structured (SQL) and unstructured (PDF, DOCX, TXT, CSV, HTML, etc.) company documents and integrates with Claude Desktop or any MCP‑compatible client to answer natural‑language questions with context‑aware responses — all without sending your data to external APIs.

---


## Demo

Quick preview (GIF):

![Demo: Semantic search + contextual answer](assets/demo.gif)


- [Full Video Demo]()

## Key Features

- **Semantic Search**: FAISS + Sentence Transformers for top‑k similarity search on local documents.  
- **Context‑Aware Answers**: Automatically retrieves and injects relevant passages into LLM prompts.  
- **Structured + Unstructured**: Query PostgreSQL and files side‑by‑side.  
- **Agentic Tools**: Exposed as MCP tools for modular, composable automation.  
- **Auto Indexing**: Optional cron job keeps your FAISS index fresh.  
- **Fully Local & Private**: No external calls; data stays on your machine.

---

## Project Structure

```
mcp-rag-toolkit/
├── data/                         # Put your company documents here
├── index/                        # FAISS index + document mapping (generated)
├── auto_updates/                 # Cron scripts & helpers
├── mcp_rag_toolkit/
│   ├── server.py                 # MCP server entrypoint
│   ├── index_document_tool.py    # One-shot indexing over /data
│   ├── update_index_tool.py      # Incremental updates based on file changes
│   ├── document_search.py        # Semantic similarity search
│   ├── read_utils.py             # File reading utilities
│   ├── file_utils.py             # Index & mapping helpers
│   ├── query_executor.py         # PostgreSQL query execution
│   ├── model_downloader.py       # SBERT model bootstrapper (optional)
│   ├── README.md
├── pyproject.toml
├── poetry.lock
```

> To use your own data, place structured and unstructured files inside the `data/` directory, e.g.:
>
> ```
> data/my_company_docs/
>   ├── hr_policies.pdf
>   ├── Q1_financial_report.xlsx
>   ├── meeting_notes.docx
>   ├── wiki_pages/
>   │   ├── operations.html
>   │   └── runbooks.md
> ```

---

## How It Works

### Tools

| MCP Tool            | Purpose                                                                           | Typical Use |
|---------------------|------------------------------------------------------------------------------------|-------------|
| `semantic_search`   | Returns top‑k most relevant documents by embedding similarity.                     | Find docs to cite |
| `read_file`         | Reads supported files and returns text + metadata.                                 | retreives info from the file |
| `query_sql`         | Executes SQL against a local PostgreSQL database.                                  | Structured lookup |
| `index_document`    | Builds FAISS index from everything in `data/`.                                     | First-time setup |
| `rag_prompt`        | Orchestrates search + reading and composes a context‑rich prompt for the LLM.      | End-to-end Q&A |

### Typical Flow

1. User asks a question in the MCP client.  
2. `rag_prompt` triggers `semantic_search` (top‑k).  
3. For the top results, `read_file` loads content snippets.  
4. The server assembles a prompt with the retrieved context.  
5. The client LLM answers, grounded in your local material.

---

## Setup

### Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/)
- FAISS (CPU) wheels installed by Poetry
- PostgreSQL (optional; only needed for `query_sql`)

### Install

```bash
# Clone
git clone git@github.com:axdithyaxo/mcp-rag-toolkit.git
cd mcp-rag-toolkit

# Install dependencies
poetry install
poetry shell

# (Optional) Pre-download the embedding model
python mcp_rag_toolkit/model_downloader.py
```

> Model weights download automatically on first use if you skip the optional step.

---

## Usage

### 1) Add Your Company Data

Supported file types include: `pdf`, `docx`, `txt`, `md`, `html`, `csv`, `json`.

Place them under `data/` (subfolders are fine).

### 2) Build the Index

```bash
python mcp_rag_toolkit/index_document_tool.py
```

This generates:
- `index/vector.index` (FAISS index)
- `index/doc_mapping.pkl` (file path mapping)

### 3) Run the MCP Server

```bash
mcp run mcp_rag_toolkit/server.py
```

Connect from Claude Desktop or an MCP inspector and start asking questions like:

```
What are the onboarding steps in our HR policies?
```

or

```
How do I restart the ZenithTech service on Ubuntu?
```

---

## Automatic Index Updates (Cron)

Keep your index fresh without manual steps.

### How It Works

- A cron entry invokes `update_index_tool.py` on a schedule.
- New or modified files in `data/` are detected and appended/updated in FAISS.
- A log file captures activity for verification.

### Example (macOS/Linux)

Edit crontab:

```bash
crontab -e
```

Add an entry to run at midnight daily:

```bash
0 0 * * * /path/to/poetry run python /absolute/path/to/mcp-rag-toolkit/mcp_rag_toolkit/update_index_tool.py >> /absolute/path/to/mcp-rag-toolkit/auto_updates/cron_debug.log 2>&1
```

Or load the provided example:

```bash
crontab auto_updates/crontab_example.txt
```

> Tip: If Poetry lives outside your default cron PATH, use an absolute interpreter like  
> `/absolute/path/to/mcp-rag-toolkit/.venv/bin/python mcp_rag_toolkit/update_index_tool.py`

---

## Tool Return Formats

### `semantic_search`

```json
{
  "query": "user query",
  "top_k": 3,
  "results": [
    "/abs/path/to/doc1.txt",
    "/abs/path/to/doc2.pdf",
    "/abs/path/to/doc3.md"
  ]
}
```

### `read_file`

```json
{
  "status": "success",
  "content": "file text here ...",
  "content_length": 1234,
  "truncated": false,
  "file_info": {
    "path": "/abs/path/to/file.txt",
    "type": "txt",
    "size": 5678,
    "encoding": "utf-8"
  }
}
```

Error example:

```json
{
  "status": "error",
  "error_code": "FILE_NOT_FOUND",
  "error_message": "File not found: /path/that/does/not/exist.txt"
}
```

### `query_sql`  (if enabled and DB reachable)

```json
{
  "columns": ["employee_id", "name", "role"],
  "rows": [[1, "Jane Doe", "Analyst"], [2, "John Smith", "Manager"]],
  "row_count": 2
}
```

Error example:

```json
{
  "error": "relation \"employee_directory\" does not exist"
}
```

---

## Models & Storage

- **Embedding model**: `sentence-transformers/all-MiniLM-L6-v2`  
- **Model cache**: `mcp_rag_toolkit/models/`  
- **FAISS index**: `index/vector.index`  
- **Document mapping**: `index/doc_mapping.pkl`

---

## PostgreSQL Configuration (Optional)

By default, `query_executor.py` uses local defaults. For production, consider environment variables:

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=zenith_tech
export PGUSER=your_user
export PGPASSWORD=your_password
```

Then adapt your connector to read from env. Keep credentials out of source control.

---

## Troubleshooting

**“Index or document mapping file not found.”**  
Run the indexer first:
```bash
python mcp_rag_toolkit/index_document_tool.py
```
Ensure `index/vector.index` and `index/doc_mapping.pkl` exist.

**Semantic search returns placeholders like “[Unknown Document #0]”.**  
Your index and mapping are out of sync. Rebuild:
```bash
python mcp_rag_toolkit/index_document_tool.py
```

**FAISS GPU constructor warnings**  
You’re using the CPU build; these warnings are harmless.

**`read_file` returns FILE_NOT_FOUND**  
Use absolute paths returned by `semantic_search`, or ensure your relative paths are from the repo root.

**Cron doesn’t run**  
Use absolute paths to `python` or `poetry` in your crontab, and check `auto_updates/cron_debug.log`.

---

## Privacy & Security

- All data stays local.  
- No external network calls required.  
- Suitable for sensitive enterprise environments.

---

## License

MIT License © 2025 Aadithya Vishnu Sajeev

---

## Acknowledgements

- Model Context Protocol  
- FAISS  
- SentenceTransformers  
- Claude AI / Anthropic
