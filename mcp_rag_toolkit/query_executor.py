# query_executor.py
import psycopg2
import pandas as pd

def run_sql_query(sql: str) -> dict:
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="zenith_tech",
            user="aadithya",
            password="",
            port=5432
        )
        df = pd.read_sql(sql, conn)
        return {
            "columns": df.columns.tolist(),
            "rows": df.values.tolist(),
            "row_count": len(df),
            "error": None
        }

    except Exception as e:
        return {
            "columns": [],
            "rows": [],
            "row_count": 0,
            "error": str(e)
        }

    finally:
        if conn:
            conn.close()