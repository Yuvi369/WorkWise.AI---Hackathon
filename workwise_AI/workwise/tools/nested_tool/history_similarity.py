import sys
import os

# Dynamically add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from crewai.tools import BaseTool
from workwise.tools.get_emp_history_tool import get_employee_history
from workwise.tools.calc_similarity_tool import calculate_similarity
from workwise.tools.nested_tool.normalize_enrich_skills import NormalizeAndEnrichSkillsTool

class EmployeeHistoryAndSimilarityTool(BaseTool):
    name: str = "Employee History and Similarity Calculator"
    description: str = "Fetches employee history based on normalized and enriched skills and calculates similarity scores for a given ticket description and skills."

    def _run(self, emp_list: list, description: str, skills: list, ticket_name: str) -> tuple:
        """
        Normalizes and enriches skills, retrieves employee history, and calculates similarity scores.
        
        Args:
            emp_list (list): List of employee IDs or details.
            description (str): Description of the ticket or task.
            skills (list): List of required skills.
            ticket_name (str): Name of the ticket or task.
        
        Returns:
            tuple: Enriched similarity scores and employee history.
        """
        # Normalize and enrich skills
        normalize_and_enrich = NormalizeAndEnrichSkillsTool()
        get_skills = normalize_and_enrich._run(skills, description)

        # Get employee history
        history = get_employee_history.func(emp_list, get_skills)
        
        # Calculate similarity
        enriched = calculate_similarity.func(ticket_name, description, get_skills)
        
        return enriched, history

if __name__ == "__main__":
    # Example usage
    emp_list = ["emp1", "emp2", "emp3"]
    description = "Fix button layout issues and apply responsive design in LWC component."
    skills = ['JavaScript', 'LWC', 'CSS', 'Python', 'Vue']
    ticket_name = "LWC_Button_Fix"
    tool = EmployeeHistoryAndSimilarityTool()
    result = tool._run(emp_list, description, skills, ticket_name)
    print(result)