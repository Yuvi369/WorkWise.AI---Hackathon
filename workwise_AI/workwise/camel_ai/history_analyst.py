# get_emp_tools.py - Fixed Version

from base_agent import BaseAgent, Message, MessageType, Tool
from tools_camel.get_emp_history_tool import get_employee_history
from tools_camel.calc_similarity_tool import calculate_similarity
import json
import time

# Create tool wrappers for the agent
class EmployeeHistoryTool(Tool):
    def __init__(self):
        super().__init__("get_employee_history", "Fetches employee history based on skills")
    
    def execute(self, params):
        employees = params.get("employees", [])
        skills = params.get("skills", [])
        return get_employee_history(employees, skills)

class SimilarityTool(Tool):
    def __init__(self):
        super().__init__("calculate_similarity", "Calculates similarity between ticket and requirements")
    
    def execute(self, params):
        ticket_name = params.get("ticket_name", "")
        description = params.get("description", "")
        skills = params.get("skills", [])
        return calculate_similarity(ticket_name, description, skills)

class HistoryAnalyst(BaseAgent):
    def __init__(self):
        super().__init__(
            name="history_analyzer",
            role="Employee Ticket History Evaluator",
            specialization="""You are the company's internal historian — an expert at spotting patterns in project history.
                        You've reviewed thousands of past tickets and know exactly which employees shine in which kinds of tasks.
                        You use this wisdom to match the right person to the right task based on what they've solved before.
                      """
        )

        print("*****^^^^^^####### History Analyzer agent execution Started *****^^^^^^#######")
        
        # Register tools with the agent
        self.add_tool(EmployeeHistoryTool())
        self.add_tool(SimilarityTool())

    def analyze_employee_for_ticket(self, tkt_name: str, tkt_description: str, skill_set: list, employees: list) -> dict:
        """Direct analysis method (bypasses agent messaging system)"""
        print(f"🔍 Analyzing ticket: {tkt_name}")
        print(f"📋 Description: {tkt_description}")
        print(f"🎯 Required skills: {skill_set}")
        print(f"👥 Employees to evaluate: {employees}")
        print("-" * 50)
        
        try:
            # Fetch employee history
            print("📚 Fetching employee history...")
            fetch_history = get_employee_history(employees, skill_set)
            print(f"✅ History retrieved: {fetch_history}")
            
            # Calculate similarity
            print("🔬 Calculating similarity scores...")
            similarity = calculate_similarity(tkt_name, tkt_description, skill_set)
            print(f"✅ Similarity calculated: {similarity}")
            
            result = {
                "history_found": fetch_history,
                "calculated_similarity": similarity
            }
            
            print("-" * 50)
            print("📊 ANALYSIS COMPLETE")
            print(f"📋 Final Result: {json.dumps(result, indent=2)}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            print(error_msg)
            return {
                "error": str(e),
                "history_found": None,
                "calculated_similarity": None
            }

    def analyze_with_agent_system(self, tkt_name: str, tkt_description: str, skill_set: list, employees: list):
        """Uses the agent's messaging system (more advanced)"""
        
        # Create a task message
        task_content = f"""
        Please analyze this ticket for employee assignment:
        
        Ticket: {tkt_name}
        Description: {tkt_description}
        Required Skills: {skill_set}
        Available Employees: {employees}

        call get_employee_history tool with "Available Employees" with "Required Skills"- it returns the employee previous ticket history's.
        call calculate_similarity tool with "Ticket","Description" with "Required Skills"- it calculates the score employee previous ticket history's and the current ticket. 
        
        Use the get_employee_history and calculate_similarity tools to provide a comprehensive analysis.
        """
        
        message = Message(
            sender="system",
            receiver=self.name,
            message_type=MessageType.TASK_ASSIGNMENT,
            content=task_content,
            timestamp=time.time()
        )
        
        print(f"📨 Sending task to agent: {self.name}")
        print(f"📝 Task: {task_content}")
        
        # Process the message
        response = self.process_message(message)
        
        if response:
            print(f"🤖 Agent Response:")
            print(f"📤 From: {response.sender}")
            print(f"📥 To: {response.receiver}")
            print(f"📋 Type: {response.message_type}")
            print(f"💬 Content: {response.content}")
            print("*****^^^^^^####### history Analyzer agent execution Completed *****^^^^^^#######")
            return response
        else:
            print("❌ No response from agent")
            return None

if __name__ == "__main__":
    print("🚀 Starting HistoryAnalyst Test")
    print("=" * 60)
    
    try:
        analyst = HistoryAnalyst()
        print("✅ HistoryAnalyst created successfully")
        print(f"🔧 Available tools: {list(analyst.tools.keys())}")
        
        # Test data
        test_ticket_name = "Database Backup Automation"
        test_description = "Set up automated daily backups for the production database to an S3 bucket."
        test_skills = ["AWS", "S3", "cloud computing", "storage services", "database management"]
        employee_profile = [
            "Mark Jenkins",
            "Kenneth Green", 
            "Amanda Lewis"
        ]
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 1: Direct Analysis (Bypasses Agent System)")
        print("=" * 60)
        
        result1 = analyst.analyze_employee_for_ticket(
            test_ticket_name, 
            test_description, 
            test_skills, 
            employee_profile
        )
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 2: Agent System Analysis (Uses Messaging)")
        print("=" * 60)
        
        result2 = analyst.analyze_with_agent_system(
            test_ticket_name,
            test_description, 
            test_skills,
            employee_profile
        )
        
        print("\n" + "=" * 60)
        print("🏁 TEST COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 MAIN ERROR: {e}")
        import traceback
        traceback.print_exc()