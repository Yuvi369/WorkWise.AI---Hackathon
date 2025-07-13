from langchain.tools import tool
import json
from datetime import datetime
import os

@tool
def log_assignment(ticket_info: dict, selected_employee: str, reasoning: str, score: int = None) -> str:
    """
    Logs the final ticket assignment to a local JSONL file.
    
    Args:
        ticket_info (dict): The ticket details like ID, title, department.
        selected_employee (str): The name of the assigned employee.
        reasoning (str): Explanation why the employee was chosen.
        score (int, optional): Similarity or confidence score (0–100).
    
    Returns:
        str: Success or failure message.
    """
    try:
        record = {
            "timestamp": datetime.now().isoformat(),
            "ticket_id": ticket_info.get("ticket_id"),
            "ticket_title": ticket_info.get("ticket_name"),
            "department": ticket_info.get("department"),
            "employee_name": selected_employee,
            "score": score,
            "reasoning": reasoning
        }

        # ✅ Log to JSONL file
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", "assignment_log.jsonl")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        print("📁 Logged file path:", os.path.abspath(log_path))

        return "✅ Assignment logged to file successfully"

    except Exception as e:
        print("❌ Error logging assignment:", e)
        return "❌ Failed to log assignment"

if __name__ == "__main__":
    ticket_info = {
        "ticket_id": "AA-204",
        "ticket_name": "Fix LWC Bug in Finance Dashboard",
        "department": "Development"
    }

    result = log_assignment.func(
        ticket_info,
        selected_employee="Vasanth",
        reasoning="Strong match on LWC skills and past tickets. Availability confirmed.",
        score=92
    )

    print(result)
