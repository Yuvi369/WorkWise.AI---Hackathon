# get_policy_tools.py - Complete Agent Implementation

from base_agent import BaseAgent, Message, MessageType, Tool
from tools_camel.rag_policy_check import rag_policy_checker
import json
import time

# Create tool wrapper for the agent
class PolicyCheckTool(Tool):
    def __init__(self):
        super().__init__("rag_policy_checker", "Checks HR policy compliance using RAG system")
        print("*****^^^^^^####### Policy Analyzer agent execution Started *****^^^^^^#######")
    
    def execute(self, params):
        ticket_name = params.get("ticket_name", "")
        ticket_id = params.get("ticket_id", "")
        ticket_description = params.get("ticket_description", "")
        employee_profile = params.get("employee_profile", [])
        emp_db = params.get("emp_db", "")
        col = params.get("col", "")
        return rag_policy_checker(ticket_name, ticket_id, ticket_description, employee_profile, emp_db, col)

class PolicyChecker(BaseAgent):
    def __init__(self):
        super().__init__(
            name="policy_checker",
            role="HR Policy Compliance Validator",
            specialization="""You are the digital guardian of HR policy.
                         You've memorized every internal rule, exception, and sensitive domain restriction.
                        You operate through a powerful RAG system that lets you recall the right rule at the right time.
                         Your mission is to ensure every assignment is not only optimal — but also compliant, secure, and ethical.
                      """
        )
        
        # Register tool with the agent
        self.add_tool(PolicyCheckTool())

    def analyze_hr_policy(self, ticket_name: str, ticket_id: str, ticket_description: str, employee_profile: dict, emp_db: str, col: str) -> dict:
        """Direct analysis method (bypasses agent messaging system)"""
        print(f"🔍 Analyzing policy compliance for ticket: {ticket_name}")
        print(f"🎫 Ticket ID: {ticket_id}")
        print(f"📋 Description: {ticket_description}")
        print(f"👥 Employee profiles: {len(employee_profile) if isinstance(employee_profile, list) else 1}")
        print(f"📊 Database: {emp_db}")
        print(f"🔍 Column: {col}")
        print("-" * 50)
        
        try:
            # Run policy check
            print("🛡️ Running policy compliance check...")
            policy_check_results = rag_policy_checker(
                ticket_name,
                ticket_id,
                ticket_description,
                employee_profile,
                emp_db,
                col
            )
            print(f"✅ Policy check completed: {policy_check_results}")
            
            result = {
                "policy_check_results": policy_check_results
            }
            
            print("-" * 50)
            print("📊 POLICY ANALYSIS COMPLETE")
            print(f"📋 Final Result: {json.dumps(result, indent=2)}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during policy analysis: {str(e)}"
            print(error_msg)
            return {
                "error": str(e),
                "policy_check_results": None
            }

    def analyze_with_agent_system(self, ticket_name: str, ticket_id: str, ticket_description: str, employee_profile: dict, emp_db: str, col: str):
        """Uses the agent's messaging system (more advanced)"""
        
        # Prepare safe parameters for the agent
        safe_emp_db = emp_db.replace("\\", "/")  # Convert backslashes to forward slashes
        emp_profile_str = json.dumps(employee_profile)  # Properly serialize employee profiles
        
        # Create a task message with cleaner parameter formatting
        task_content = f"""
        Please analyze this ticket for HR policy compliance:
        
        Ticket Name: {ticket_name}
        Ticket ID: {ticket_id}
        Description: {ticket_description}
        Employee Count: {len(employee_profile) if isinstance(employee_profile, list) else 1}
        Database Path: {safe_emp_db}
        Column: {col}

        Use the rag_policy_checker tool with these exact parameters:
        - ticket_name: "{ticket_name}"
        - ticket_id: "{ticket_id}" 
        - ticket_description: "{ticket_description}"
        - employee_profile: {emp_profile_str}
        - emp_db: "{safe_emp_db}"
        - col: "{col}"

        Validate HR policy compliance for this ticket assignment and provide a comprehensive analysis.
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
            print("*****^^^^^^####### Policy Analyzer agent execution Completed *****^^^^^^#######")
            return response
        else:
            print("❌ No response from agent")
            return None

if __name__ == "__main__":
    print("🚀 Starting PolicyChecker Test")
    print("=" * 60)
    
    try:
        analyst = PolicyChecker()
        print("✅ PolicyChecker created successfully")
        print(f"🔧 Available tools: {list(analyst.tools.keys())}")
        
        # Test data
        ticket_name = "UI Production fix"
        ticket_id = "FD - 0089"
        ticket_description = "Fix UI padding and button alignment in LWC component."
        
        # Fixed the employee_profile structure (was incorrectly using set syntax)
        employee_profile = [
            {
                "employee_name": "Kenneth Simpson",
                "designation": "Intern",
                "department": "Development",
                "availability": "Available"
            },
            {
                "employee_name": "1234yuva",  # This should be skipped (not in Excel)
                "designation": "Intern",
                "department": "Development",
                "availability": "Unavailable"
            },
            {
                "employee_name": "Mark Jenkins",
                "designation": "Senior Developer",
                "department": "Development",
                "availability": "Available"
            }
        ]
        
        emp_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employee_with_ids.xlsx"
        col = "name"
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 1: Direct Analysis (Bypasses Agent System)")
        print("=" * 60)
        
        result1 = analyst.analyze_hr_policy(
            ticket_name,
            ticket_id,
            ticket_description,
            employee_profile,
            emp_db,
            col
        )
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 2: Agent System Analysis (Uses Messaging)")
        print("=" * 60)
        
        result2 = analyst.analyze_with_agent_system(
            ticket_name,
            ticket_id,
            ticket_description,
            employee_profile,
            emp_db,
            col
        )
        
        print("\n" + "=" * 60)
        print("🏁 TEST COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 MAIN ERROR: {e}")
        import traceback
        traceback.print_exc()