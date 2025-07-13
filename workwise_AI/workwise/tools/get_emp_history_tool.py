import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from langchain.tools import tool

# Load .env
load_dotenv()

@tool
def get_employee_history(employee_name: str) -> list:
    """
    Fetches ticket history for a given employee from PostgreSQL.
    Returns a list of ticket dictionaries with id, title, type, skills, etc.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT ticket_id, title, type, skills_used, priority, duration_days, status
                FROM employee_history
                WHERE employee_name = %s
                ORDER BY created_at DESC
            """, (employee_name,))
            
            rows = cur.fetchall()
            return [dict(row) for row in rows]

    except Exception as e:
        print("❌ DB Query Failed:", e)
        return []

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    history = get_employee_history.func("Vasanth")
    print("📜 History:", history)
