![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Build](https://github.com/yourgithubusername/mcp-rag-toolkit/actions/workflows/ci.yml/badge.svg)

# MCP RAG Toolkit

**MCP RAG Toolkit** is a secure, AI-augmented local Retrieval-Augmented Generation server built using the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol). It integrates structured SQL data and unstructured document search with semantic retrieval to provide accurate and context-aware responses to natural language queries.

---

## Features

* Semantic document retrieval over enterprise documents (PDF, DOCX, TXT, CSV, Markdown, HTML)
* Structured SQL querying for company databases (e.g., employee directory, budgets)
* Flexible file reading with support for multiple formats including PDF (via PyMuPDF) and DOCX
* Logging of accessed files for auditability
* Easy integration with Claude Desktop and other LLMs via MCP
* Secure sandboxed environment with path restrictions

---

## Screenshot

![Demo Screenshot](assets/demo_screenshot.png)

---

## Getting Started

### Prerequisites

* Python 3.10+
* Poetry or pip for dependency management
* MCP CLI (`pip install modelcontext`)

### Installation

Using Poetry (recommended):

```bash
git clone https://github.com/yourgithubusername/mcp-rag-toolkit.git
cd mcp-rag-toolkit

curl -sSL https://install.python-poetry.org | python3 -

poetry install
poetry shell

cp .env.example .env
# Edit .env to configure environment variables (e.g. data directories)
```

Or using Python venv and pip:

```bash
git clone https://github.com/yourgithubusername/mcp-rag-toolkit.git
cd mcp-rag-toolkit

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env as needed
```

---

## Usage

### Starting the Server

Make sure MCP CLI is installed (`pip install modelcontext`) and dependencies are installed.

Run the server:

```bash
mcp dev mcp_rag_toolkit/server.py
```

### Accessing via MCP Inspector

Open:

```
http://127.0.0.1:6274
```

Here you can:

* Run tools like `retrieve_docs`, `query_sql`, `read_file`
* Execute custom prompts
* Inspect structured output and logs

---

## Example Prompts

**Retrieve documents:**

> Find latest HR policies and FAQs.

**Query SQL:**

> Show first 5 employees in the HR department.

**Read file:**

> Read the contents of `hr/Employee_Benefits_2024.pdf`.

---

## Project Structure

```
mcp_rag_toolkit/
├── data/                        # Enterprise documents and CSVs
├── index/                       # FAISS index and logs
├── logs/                        # Access logs
├── mcp_rag_toolkit/             # Source code
│   ├── __init__.py
│   ├── document_search.py       # Document retrieval & reading
│   ├── query_executor.py        # SQL query execution
│   ├── server.py                # MCP server and tools
│   └── ...
├── tests/                       # Unit tests
├── README.md
└── pyproject.toml / requirements.txt
```

---

## Environment Variables

| Variable    | Description                            |
| ----------- | ---------------------------------- |
| `DATA_ROOT` | Base directory for enterprise files |
| `SAFE_BASE` | Root path restricting file access    |

---

## Contributing

Contributions welcome! Please submit pull requests or open issues.

---

## License

MIT License

---

## Acknowledgments

* Model Context Protocol (MCP) project and community  
* FastMCP Python SDK maintainers  
* Open-source contributors for document parsing libraries  
* The broader AI and enterprise search community  

---

## Demo Video

Watch a demo video here:

[Demo Video](https://yourlink.com/demo)