import psycopg2
import pandas as pd

def run_sql_query(query: str) -> pd.DataFrame:
    """
    Connects to the PostgreSQL database and executes the provided SQL query.

    Args:
        query (str): SQL query string to execute.

    Returns:
        pd.DataFrame: Resulting data as a Pandas DataFrame.
    """
    conn = None
    try:
        # Establish the database connection
        conn = psycopg2.connect(
            host="localhost",
            database="zenith_tech",
            user="aadithya",
            password="",  # Provide password if needed
            port=5432
        )

        # Use context manager for the connection to ensure closure
        with conn.cursor() as cursor:
            df = pd.read_sql(query, conn)

        return df

    except Exception as e:
        print(f"[ERROR] Failed to run query: {e}")
        # You may want to re-raise or handle differently
        return pd.DataFrame()

    finally:
        if conn is not None:
            conn.close()