from mcp.server.fastmcp import FastMCP
from mcp_rag_toolkit.query_executor import run_sql_query
import os
import pickle
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text

import logging

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "..", "index", "claude_access.log"),
    level=logging.INFO,
    format="%(asctime)s - [READ FILE] Claude accessed: %(message)s"
)

# --- Document-based retrieval tool ---
from mcp_rag_toolkit.document_search import search_documents

# Initialize the MCP server with dependencies
mcp = FastMCP("ZenithTechRAG", dependencies=[
    "pandas", "psycopg2-binary"
])

import json
from mcp_rag_toolkit.document_search import search_documents

import json
import os
from mcp_rag_toolkit.document_search import search_documents



import json

import json

@mcp.tool()
def retrieve_docs(question: str) -> str:
    """
    Retrieve document snippets related to the user's question using semantic similarity.
    Returns a JSON string with documents, metadata, scores, and timing info.
    """
    results = search_documents(question)
    return json.dumps(results, indent=2)


@mcp.tool()
def query_sql(sql: str) -> str:
    """
    Execute a raw SQL query on the underlying PostgreSQL database.

    IMPORTANT:
    - This tool works ONLY with PostgreSQL.
    - Using other SQL dialects (e.g., SQLite) may cause syntax errors.
    
    Args:
        sql (str): A valid PostgreSQL SQL query string.
    
    Returns:
        str: JSON string containing:
            - columns: list of column names
            - rows: list of rows (each a list of column values)
            - row_count: number of rows returned
            - error: optional, error message if query fails
    """
    try:
        df = run_sql_query(sql)
        if df is None or df.empty:
            return json.dumps({
                "columns": [],
                "rows": [],
                "row_count": 0
            })

        columns = list(df.columns)
        rows = df.values.tolist()
        row_count = len(df)

        return json.dumps({
            "columns": columns,
            "rows": rows,
            "row_count": row_count
        })

    except Exception as e:
        return json.dumps({
            "columns": [],
            "rows": [],
            "row_count": 0,
            "error": str(e)
        })

@mcp.resource("sql://generate/{prompt}")
def generate_sql(prompt: str) -> str:
    """
    You are working with a PostgreSQL database. Here's the schema of the `employee_directory` table:

    Table: employee_directory
    Columns:
    - employee_id (INT)
    - name (TEXT)
    - role (TEXT)
    - department (TEXT)
    - email (TEXT)

    Use this information to convert natural language queries into SQL statements.

    This function is a stub—handled by Claude via prompt injection or resource calls.
    """
    raise NotImplementedError("Handled by Claude or prompt injection.")


# --- Resource describing combined data capabilities ---
@mcp.resource("data://overview")
def data_overview() -> str:
    """
    Describes available data sources for Claude: SQL and document-based.

    Returns:
        str: A description of what Claude can query.
    """
    return (
        "This RAG system has access to structured SQL data (e.g., employee_directory, department_budgets_2023) "
        "and unstructured documents stored in the local data/ folder. "
        "Use `query_sql(sql: str)` to query SQL tables or `retrieve_docs(question: str)` to retrieve text from documents."
    )

import os
import logging
import json
from docx import Document

import os
import json
import logging
from docx import Document

@mcp.tool()
def read_file(path: str) -> str:
    """
    Read the full content of a given document path and return JSON response.

    Supports both:
    - Full paths as returned by list_indexed_files (e.g., data/enterprise_rag_sample_docs_v3/hr/...)
    - Relative paths from base data directory (e.g., hr/...)

    Args:
        path (str): Document path, either full or relative.

    Returns:
        JSON string with either:
          - {"content": "...file contents...", "path": "..."}
          - {"error": "...error message..."}
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "enterprise_rag_sample_docs_v3"))

    # Determine full path, support full paths from list_indexed_files
    if path.startswith("data/enterprise_rag_sample_docs_v3"):
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path))
    else:
        full_path = os.path.abspath(os.path.join(base_dir, path))

    if not os.path.isfile(full_path):
        error_msg = f"⚠️ File not found: {full_path}"
        logging.warning(error_msg)
        return json.dumps({"error": error_msg})

    try:
        if full_path.endswith(".docx"):
            doc = Document(full_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            if not paragraphs:
                error_msg = f"⚠️ The document {path} is empty or contains no readable text."
                logging.warning(error_msg)
                return json.dumps({"error": error_msg})
            content = "\n".join(paragraphs)
            logging.info(f"Read DOCX file: {full_path}")
            return json.dumps({"content": content, "path": path})

        elif full_path.endswith(".pdf"):
            import fitz  # PyMuPDF
            doc = fitz.open(full_path)
            content = "\n".join(page.get_text() for page in doc)
            if not content.strip():
                error_msg = f"⚠️ The PDF {path} is empty or contains no readable text."
                logging.warning(error_msg)
                return json.dumps({"error": error_msg})
            logging.info(f"Read PDF file: {full_path}")
            return json.dumps({"content": content, "path": path})

        else:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                error_msg = f"⚠️ The file {path} is empty."
                logging.warning(error_msg)
                return json.dumps({"error": error_msg})
            logging.info(f"Read text file: {full_path}")
            return json.dumps({"content": content, "path": path})

    except Exception as e:
        error_msg = f"⚠️ Failed to read file {path}: {e}"
        logging.error(error_msg)
        return json.dumps({"error": error_msg})




# --- MCP tool: List indexed and skipped files ---
@mcp.tool()
def list_indexed_files() -> str:
    indexed_files = []
    skipped_files = []

    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "index", "doc_texts.pkl"), "rb") as f:
            indexed_files = pickle.load(f)
    except Exception as e:
        indexed_files = []

    try:
        log_path = os.path.join(os.path.dirname(__file__), "..", "index", "index_log.txt")
        if os.path.exists(log_path):
            with open(log_path, "r") as logf:
                skipped_files = [line.strip().split("⚠️ Skipped:")[-1].strip() for line in logf if "⚠️ Skipped:" in line]
    except Exception as e:
        skipped_files = []

    return json.dumps({
        "indexed_files": indexed_files,
        "skipped_files": skipped_files,
        "total_indexed": len(indexed_files),
        "total_skipped": len(skipped_files),
        "index_status": "complete" if indexed_files else "empty"
    })
