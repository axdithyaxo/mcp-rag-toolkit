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

@mcp.tool()
def retrieve_docs(question: str) -> str:
    """
    Retrieve document snippets related to the user's question using semantic similarity.

    Args:
        question (str): A user’s natural language question.

    Returns:
        str: Relevant document snippets retrieved from the corpus.
    """
    return search_documents(question)

@mcp.tool()
def query_sql(sql: str) -> str:
    """
    Execute a raw SQL query on the underlying structured data source.

    Args:
        sql (str): A valid SQL query string.

    Returns:
        str: Tabulated markdown output of the query result.

    Example:
        >>> query_sql("SELECT name FROM employee_directory WHERE department = 'IT';")
    """
    df = run_sql_query(sql)
    return df.to_markdown()

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

@mcp.tool()
def read_file(path: str) -> str:
    """
    Read the full content of a given document path.
    """
    try:
        # Normalize relative to project root
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "enterprise_rag_sample_docs_v3"))
        full_path = os.path.abspath(os.path.join(base_dir, path))

        if not os.path.isfile(full_path):
            return f"⚠️ File not found: {full_path}"

        if full_path.endswith(".docx"):
            try:
                doc = Document(full_path)
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                if not paragraphs:
                    return f"⚠️ The document {path} is empty or contains no readable text."
                logging.info(full_path)
                return "\n".join(paragraphs)
            except Exception as e:
                return f"⚠️ Failed to read DOCX file {path}: {e}"
        elif full_path.endswith(".pdf"):
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(full_path)
                content = "\n".join(page.get_text() for page in doc)
                if not content.strip():
                    return f"⚠️ The PDF {path} is empty or contains no readable text."
                logging.info(full_path)
                return content
            except Exception as e:
                return f"⚠️ Failed to read PDF file {path}: {e}"
        else:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                logging.info(full_path)
                return content
    except Exception as e:
        return f"⚠️ Could not read file: {e}"
server = mcp


# --- MCP tool: List indexed and skipped files ---
@mcp.tool()
def list_indexed_files() -> str:
    """
    Returns a summary of indexed and skipped files from FAISS indexing logs.
    Useful for debugging document inclusion/exclusion for RAG.
    """
    indexed_files = []
    skipped_files = []

    try:
        # Load indexed file paths
        with open(os.path.join(os.path.dirname(__file__), "..", "index", "doc_texts.pkl"), "rb") as f:
            indexed_files = pickle.load(f)
    except Exception as e:
        indexed_files = [f"⚠️ Could not read doc_texts.pkl: {e}"]

    try:
        # Parse skipped files from index_log.txt
        log_path = os.path.join(os.path.dirname(__file__), "..", "index", "index_log.txt")
        if os.path.exists(log_path):
            with open(log_path, "r") as logf:
                skipped_files = [line.strip().split("⚠️ Skipped:")[-1].strip() for line in logf if "⚠️ Skipped:" in line]
    except Exception as e:
        skipped_files = [f"⚠️ Could not read index_log.txt: {e}"]

    report = f"✅ Indexed Files ({len(indexed_files)}):\n" + "\n".join(f"- {p}" for p in indexed_files)
    report += f"\n\n❌ Skipped Files ({len(skipped_files)}):\n" + ("\n".join(f"- {p}" for p in skipped_files) if skipped_files else "None logged.")
    return report
