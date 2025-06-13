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
    try:
        # Establish the database connection
        conn = psycopg2.connect(
            host="localhost",
            database="zenith_tech",
            user="aadithya",
            password="",  # Fill in if needed
            port=5432
        )

        # Execute the query and fetch results into a DataFrame
        df = pd.read_sql(query, conn)

        # Close the connection
        conn.close()

        return df.to_dict(orient="records")

    except Exception as e:
        print(f"[ERROR] Failed to run query: {e}")
        return {"error": str(e)}