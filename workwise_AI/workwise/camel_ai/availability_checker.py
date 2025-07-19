# get_availability_tools.py - Complete Agent Implementation

import os
import json
import pandas as pd
from datetime import datetime
from base_agent import BaseAgent, Message, MessageType, Tool
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import List
from tools_camel.availability_report import generate_html_report
import time

# Step 1: Define the Pydantic schema
class AvailabilityInput(BaseModel):
    employee_names: List[str] = Field(..., description="List of employee names to check")
    leave_db: str = Field(..., description="Path to the leave Excel file")
    emp_db: str = Field(..., description="Path to the employee Excel file")


def check_availability(employee_names: List[str], leave_db: str, emp_db: str) -> list:
    """
    Checks if each employee is currently available based on HRMS data.
    Returns a list of status dicts for each employee.
    """
    try:
        employee_df = pd.read_excel(emp_db)
        leave_df = pd.read_excel(leave_db)
        current_date = datetime.now().date()
        results = []
        
        for employee_name in employee_names:
            result = {"employee_name": employee_name}
            employee_row = employee_df[employee_df['name'].str.strip().str.lower() == employee_name.strip().lower()]
            
            if employee_row.empty:
                result["status"] = "error"
                result["message"] = f"Employee '{employee_name}' not found in employee database"
                results.append(result)
                continue
            
            employee_id = employee_row.iloc[0]['id']
            leave_row = leave_df[leave_df['employee_id'] == employee_id]
            
            if leave_row.empty:
                result["status"] = "available"
                result["message"] = "Employee available for assigning tickets"
                results.append(result)
                continue
            
            confirmed_leaves = leave_row[leave_row['state'].str.strip().str.lower() == 'confirm']
            
            if confirmed_leaves.empty:
                result["status"] = "available"
                result["message"] = "Employee available for assigning tickets"
                results.append(result)
                continue
            
            employee_on_leave = False
            return_date = None
            
            for _, leave in confirmed_leaves.iterrows():
                if pd.notna(leave['date_to']):
                    if isinstance(leave['date_to'], str):
                        date_to = datetime.strptime(leave['date_to'], '%Y-%m-%d').date()
                    else:
                        date_to = leave['date_to'].date() if hasattr(leave['date_to'], 'date') else leave['date_to']
                    
                    if current_date <= date_to:
                        employee_on_leave = True
                        if return_date is None or date_to > return_date:
                            return_date = date_to
            
            if employee_on_leave:
                next_available_date = return_date + pd.Timedelta(days=1)
                result["status"] = "unavailable"
                result["message"] = f"Employee unavailable till {next_available_date.strftime('%d-%m-%Y')}"
            else:
                result["status"] = "available"
                result["message"] = "Employee available for assigning tickets"
            
            results.append(result)
            
    except FileNotFoundError as e:
        return [{"status": "error", "message": f"Excel file not found: {e}"}]
    except Exception as e:
        return [{"status": "error", "message": f"Error processing data: {str(e)}"}]
    
    generate_html_report(results)
    return results

# Create tool wrapper for the agent
class AvailabilityCheckTool(Tool):
    def __init__(self):
        super().__init__("check_availability", "Checks employee availability based on HRMS data")
    
    def execute(self, params):
        employee_names = params.get("employee_names", [])
        leave_db = params.get("leave_db", "")
        emp_db = params.get("emp_db", "")
        return check_availability(employee_names, leave_db, emp_db)

class AvailabilityCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="availability_checker",
            role="Employee Availability Agent",
            specialization="""You check HRMS data to determine if employees are available or on leave today.
                           You use employee and leave records to decide availability and generate comprehensive reports.
                           You are the gatekeeper of workforce scheduling, ensuring no tickets are assigned to unavailable employees.
                         """
        )

        print("*****^^^^^^####### Availability Checker agent execution Started *****^^^^^^#######")
        
        # Register tool with the agent
        self.add_tool(AvailabilityCheckTool())

    def run_check(self, employee_names: List[str], leave_db: str, emp_db: str) -> list:
        """Direct check method (bypasses agent messaging system)"""
        print(f"🔍 Checking availability for employees: {employee_names}")
        print(f"📊 Leave database: {leave_db}")
        print(f"📊 Employee database: {emp_db}")
        print("-" * 50)
        
        try:
            # Run availability check
            print("⏰ Running availability check...")
            result = check_availability(employee_names, leave_db, emp_db)
            print(f"✅ Availability check completed")
            
            print("-" * 50)
            print("📊 AVAILABILITY CHECK COMPLETE")
            print(f"📋 Results: {json.dumps(result, indent=2)}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during availability check: {str(e)}"
            print(error_msg)
            return [{"status": "error", "message": str(e)}]

    def _safe_execute_availability_check(self, employee_names: List[str], leave_db: str, emp_db: str):
        """Safe wrapper for availability check execution with proper parameter handling"""
        try:
            # Create safe parameters
            safe_params = {
                "employee_names": employee_names,
                "leave_db": leave_db.replace("\\", "/"),  # Fix path separators
                "emp_db": emp_db.replace("\\", "/")       # Fix path separators
            }
            
            # Execute the tool directly
            tool = self.tools.get("check_availability")
            if tool:
                result = tool.execute(safe_params)
                return result
            else:
                return [{"status": "error", "message": "Availability checker tool not found"}]
                
        except Exception as e:
            return [{"status": "error", "message": f"Tool execution failed: {str(e)}"}]

    def run_check_safe(self, employee_names: List[str], leave_db: str, emp_db: str) -> list:
        """Safe check method that handles parameter issues"""
        print(f"🔍 [SAFE] Checking availability for employees: {employee_names}")
        print(f"📊 Leave database: {leave_db}")
        print(f"📊 Employee database: {emp_db}")
        print("-" * 50)
        
        try:
            # Use safe execution method
            print("⏰ Running availability check (safe mode)...")
            result = self._safe_execute_availability_check(employee_names, leave_db, emp_db)
            print(f"✅ Availability check completed")
            
            print("-" * 50)
            print("📊 AVAILABILITY CHECK COMPLETE (SAFE MODE)")
            print(f"📋 Results: {json.dumps(result, indent=2)}")
            
            return result
            
        except Exception as e:
            error_msg = f"❌ Error during safe availability check: {str(e)}"
            print(error_msg)
            return [{"status": "error", "message": str(e)}]

    def check_with_agent_system(self, employee_names: List[str], leave_db: str, emp_db: str):
        """Uses the agent's messaging system (more advanced)"""
        
        # Prepare safe parameters for the agent
        safe_leave_db = leave_db.replace("\\", "/")
        safe_emp_db = emp_db.replace("\\", "/")
        emp_names_str = json.dumps(employee_names)
        
        # Create a task message with cleaner parameter formatting
        task_content = f"""
        Please check employee availability using HRMS data:
        
        Employees to check: {employee_names}
        Employee count: {len(employee_names)}
        Leave database: {safe_leave_db}
        Employee database: {safe_emp_db}

        Use the check_availability tool with these exact parameters:
        - employee_names: {emp_names_str}
        - leave_db: "{safe_leave_db}"
        - emp_db: "{safe_emp_db}"

        Check each employee's current availability status.
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
            print("*****^^^^^^####### Availability Checker agent execution Completed *****^^^^^^#######")
            return response
        else:
            print("❌ No response from agent")
            return None

if __name__ == "__main__":
    print("🚀 Starting AvailabilityCheckerAgent Test")
    print("=" * 60)
    
    try:
        agent = AvailabilityCheckerAgent()
        print("✅ AvailabilityCheckerAgent created successfully")
        print(f"🔧 Available tools: {list(agent.tools.keys())}")
        
        # Test data
        employees = ["Mark Jenkins", "Kenneth Simpson", "Anthony Wright"]
        leave_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\Final_Employees_Leave_Table.xlsx"
        emp_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employee_with_ids.xlsx"
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 1: Direct Check (Bypasses Agent System)")
        print("=" * 60)
        
        result1 = agent.run_check(employees, leave_db, emp_db)
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 1.5: Safe Check (Fixed Parameter Handling)")
        print("=" * 60)
        
        result1_safe = agent.run_check_safe(employees, leave_db, emp_db)
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 2: Agent System Check (Uses Messaging)")
        print("=" * 60)
        
        result2 = agent.check_with_agent_system(employees, leave_db, emp_db)
        
        print("\n" + "=" * 60)
        print("🏁 TEST COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 MAIN ERROR: {e}")
        import traceback
        traceback.print_exc()