import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from langchain.tools import tool

# Load environment variables
load_dotenv()

@tool
def fetch_employee_profiles(employee_names: list) -> list:
    """
    Fetches HR profile information from PostgreSQL for the given employee names.
    Returns a list of profile dictionaries.
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
            query = """
                SELECT employee_name, designation, department, skills, experience_years, availability, leave_status
                FROM hrms_employees
                WHERE lower(employee_name) = ANY(%s)
            """
            name_list = [name.lower() for name in employee_names]
            cur.execute(query, (name_list,))
            rows = cur.fetchall()

            return [dict(row) for row in rows]

    except Exception as e:
        print("❌ Error fetching employee profiles:", e)
        return []

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    employees = ["Vasanth", "Kaviya", "NonExistent"]
    result = fetch_employee_profiles.func(employees)
    print("📄 Profiles:", result)
    