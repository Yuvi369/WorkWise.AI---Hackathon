import sys
import os
import re

# Dynamically add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from workwise.tools.fetch_emp_profile_tool import fetch_employee_profiles
from workwise.tools.normalize_skills_tools import normalize_skills
from langchain.tools import tool

def extract_skills(data):
    all_skills = []
    for emp in data:
        combined = ' '.join(emp['skills_set'])
        combined = combined.replace('\n', ' ')
        # Split on common separators (.,:, or multiple spaces)
        tokens = re.split(r'[•\n,;:\.\(\)]|\s{2,}', combined)
        cleaned = [s.strip() for s in tokens if s.strip()]
        all_skills.extend(cleaned)
    return list(set(all_skills))


@tool
def fetch_and_normalize(emp_list: list) -> list:
    """
    Normalizes a given list of required skills and enriches them using LLM context.
    """

    history = fetch_employee_profiles.func(emp_list, r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_db_1.xlsx")
    cleaned_skills = extract_skills(history)
    normalized = normalize_skills.func(cleaned_skills)
    return history, normalized


if __name__ == "__main__":
    employee_profile = [
        "Mark Jenkins",
        "Kenneth Green", 
        "Amanda Lewis"
    ]

    result, get_skils  = fetch_and_normalize.func(employee_profile)
    print(get_skils)
    print(result)