from mcp.server.fastmcp import FastMCP  # Import FastMCP
from mcp_rag_toolkit.query_executor import run_sql_query

mcp = FastMCP(name="ZenithTechRAG")

@mcp.tool()
def query_sql(sql: str) -> str:
    """
Execute a raw SQL query on the underlying PostgreSQL database.

IMPORTANT:
    - This tool works ONLY with PostgreSQL.
    - Using other SQL dialects (e.g., SQLite, MySQL) may cause syntax errors.

Available tables:
    - employee_directory: Contains columns like employee_id, name, role, department, email

Example queries:
    - List tables:
        SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
    - Check columns in a table:
        SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'table_name';

Args:
    sql (str): A valid SQL query string written for PostgreSQL syntax.

Returns:
    dict: A JSON-serializable dictionary containing:
        - columns (list[str]): Column names in the result
        - rows (list[list[Any]]): Rows returned (each row as a list of values)
        - row_count (int): Number of rows returned
        - error (str, optional): Error message if the query fails
"""
    """Run a SQL query on the ZenithTech database and return the result."""
    return run_sql_query(sql)

'''
from mcp_rag_toolkit.file_utils import list_indexed_files as get_indexed_files

@mcp.tool()
def list_indexed_files() -> dict:
    """
    List all files currently indexed and available for document retrieval.

    Returns:
        dict: {
            "status": "success",
            "files": [list of filenames]
        }
        or error message.
    """
    return get_indexed_files()
'''
# Register the read_file tool
from mcp_rag_toolkit.read_utils import read_file_content

@mcp.tool()
def read_file(file_path: str) -> dict:
    """
    Read the contents of a supported file from the local file system.

    Args:
        file_path (str): Path to the file relative to the project root.

    Returns:
        dict: {
            "status": "success",
            "content": "file content as string"
        }
        or error message.
    """
    return read_file_content(file_path)

# Register the semantic_search tool
from mcp_rag_toolkit.document_search import search_similar_documents

@mcp.tool()
def semantic_search(query: str, top_k: int = 3) -> dict:
    """
    Perform a semantic search over indexed documents and return the top matching files.

    Args:
        query (str): A natural language query to search for.
        top_k (int): Number of top similar documents to return.

    Returns:
        dict: {
            "query": "original query",
            "top_k": 3,
            "results": [list of document paths]
        }
    """
    return search_similar_documents(query, top_k)

'''
@mcp.resources(path="../data", name="enterprise_docs")
def load_static_docs():
    pass '''


from mcp_rag_toolkit.document_search import search_similar_documents
from mcp_rag_toolkit.read_utils import read_file_content

@mcp.prompt()
def rag_prompt(user_input: str) -> str:
    """
    Perform semantic document search and return a prompt that includes the most relevant context
    for the assistant to answer the user's query.

    Args:
        user_input (str): The user's natural language question.

    Returns:
        str: A prompt with relevant document context and the user's question.
    """
    # Step 1: Search similar documents
    try:
        search_results = search_similar_documents(user_input, top_k=3)
        doc_paths = search_results.get("results", [])
    except Exception as e:
        return f"Error during semantic search: {e}"

    # Step 2: Read top documents
    retrieved_contexts = []
    for path in doc_paths:
        try:
            result = read_file_content(path)
            if result.get("status") == "success":
                content = result["content"].strip()
                if content:
                    retrieved_contexts.append(content)
        except Exception:
            continue

    # Step 3: Compose contextual prompt
    context_block = "\n\n".join(retrieved_contexts[:3])  # limit to avoid token bloat
    full_prompt = f"""You are an intelligent assistant helping users based on document knowledge.

Context:
{context_block}

User Question:
{user_input}

Answer:"""

    return full_prompt