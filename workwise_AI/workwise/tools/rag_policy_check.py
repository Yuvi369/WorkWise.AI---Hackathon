from langchain.tools import tool
from workwise.engines.policy_checker_engine import run_policy_check

@tool
def rag_policy_checker(ticket_description: str, employee_profile: dict) -> str:
    """
    Checks if the employee can be assigned to the ticket based on HR policies using RAG.
    Returns one of: "Allowed", "Not Allowed", "Unclear" + reason.
    """
    try:
        result = run_policy_check(ticket_description, employee_profile)
        return result
    except Exception as e:
        print("❌ RAG Policy Checker Failed:", e)
        return "Unclear - Internal error during policy check"



if __name__ == "__main__":
    ticket_description = "Fixing an apex bug in the finance dashboard for production clients."

    employee_profile = {
        "employee_name": "Divya",
        "designation": "Intern",
        "department": "Development",
        "employment_status": "Intern",
        "level": "Junior",
        "availability": "Available"
    }

    verdict = rag_policy_checker.func(ticket_description, employee_profile)
    print("🔍 Verdict:", verdict)
