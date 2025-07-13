import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from langchain.tools import tool

# Load .env
load_dotenv()

@tool
def check_availability(employee_names: list) -> list:
    """
    Checks if each employee is currently available based on HRMS data.
    Returns a list of status dicts for each employee.
    """
    results = []
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
                SELECT employee_name, availability, leave_status
                FROM hrms_employees
                WHERE lower(employee_name) = ANY(%s)
            """
            lower_names = [name.lower() for name in employee_names]
            cur.execute(query, (lower_names,))
            rows = cur.fetchall()

            for row in rows:
                status = row["availability"]
                note = row["leave_status"]
                results.append({
                    "employee_name": row["employee_name"],
                    "available": status.lower() == "available",
                    "availability": status,
                    "leave_status": note
                })

    except Exception as e:
        print("❌ Availability check failed:", e)
    
    finally:
        if conn:
            conn.close()
    
    return results

if __name__ == "__main__":
    employees = ["Vasanth", "Akash", "Yuvaraj", "Kaviya", "Sakthivel"]
    res = check_availability.func(employees)
    for r in res:
        print(r)
