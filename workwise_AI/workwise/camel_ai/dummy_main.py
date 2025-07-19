import os
import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

from chat_gemini.classify_prompt import chat_main
import os
import base64
from pathlib import Path

# Import the HTML report generator
from tools_camel.summary_report import generate_html,save_html_report_fixed_location, save_html_report
from tools_camel.dummy_tool import build_employee_profiles

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from ticket_analyzer import TicketAnalyzerAgents
from history_analyst import HistoryAnalyst
#from skill_matcher import SkillEvaluator
from tools_camel.fetch_emp_profile_tool import fetch_employee_profiles
from tools_camel.normalize_skills_tools import normalize_skills
from availability_checker import AvailabilityCheckerAgent
from policy_checker import PolicyChecker

def normalize_skills(required_skills):
    """Normalize skills (placeholder - implement based on your logic)"""
    return [skill.strip().lower() for skill in required_skills]

def fetch_employee_profiles(suggested_employee, emp_db_path):
    """Fetch employee profiles (placeholder - implement based on your logic)"""
    # This should return employee profile data
    return {"employees": suggested_employee, "profiles": "fetched"}

def serialize_agent_result(result):
    """
    Convert agent result to JSON-serializable format
    
    Args:
        result: Agent result (could be Message object, dict, or other types)
        
    Returns:
        JSON-serializable dictionary
    """
    try:
        if hasattr(result, '__dict__'):
            # If it's an object with attributes, convert to dict
            serialized = {}
            for key, value in result.__dict__.items():
                try:
                    # Try to serialize the value
                    json.dumps(value)
                    serialized[key] = value
                except (TypeError, ValueError):
                    # If value is not serializable, convert to string
                    serialized[key] = str(value)
            return serialized
        elif isinstance(result, dict):
            # If it's already a dict, check if all values are serializable
            serialized = {}
            for key, value in result.items():
                try:
                    json.dumps(value)
                    serialized[key] = value
                except (TypeError, ValueError):
                    serialized[key] = str(value)
            return serialized
        elif isinstance(result, (list, tuple)):
            # Handle lists and tuples
            serialized = []
            for item in result:
                try:
                    json.dumps(item)
                    serialized.append(item)
                except (TypeError, ValueError):
                    serialized.append(str(item))
            return serialized
        else:
            # For other types, convert to string
            return str(result)
    except Exception as e:
        print(f"⚠️  Warning: Could not serialize agent result: {e}")
        return {"error": f"Serialization failed: {str(e)}", "raw_content": str(result)[:500]}

def get_final_employee_recommendation(agent_results: Dict[str, Any], 
                                    ticket_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send all agent results to Gemini API and get final employee recommendation
    
    Args:
        agent_results: Dictionary containing all 5 agent results
        ticket_info: Dictionary containing ticket information
        
    Returns:
        Dictionary with recommended employee and reasoning
    """
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Serialize all agent results to ensure JSON compatibility
        serialized_results = {}
        for agent_name, result in agent_results.items():
            print(f"📝 Serializing {agent_name} result...")
            serialized_results[agent_name] = serialize_agent_result(result)
        
        # Create comprehensive prompt for Gemini
        prompt = f"""
You are an expert AI system for employee assignment decisions. I will provide you with analysis results from 5 different specialized agents that have evaluated a ticket assignment scenario. Your task is to analyze all the information and recommend the BEST employee for this assignment.

TICKET INFORMATION:
- Ticket Name: {ticket_info.get('name', 'N/A')}
- Ticket ID: {ticket_info.get('id', 'N/A')}
- Description: {ticket_info.get('description', 'N/A')}
- Priority: {ticket_info.get('priority', 'N/A')}
- Due Date: {ticket_info.get('due_date', 'N/A')}
- Required Skills: {ticket_info.get('required_skills', [])}
- Suggested Employees: {ticket_info.get('suggested_employees', [])}

AGENT ANALYSIS RESULTS:

1. TICKET ANALYZER AGENT RESULT:
{json.dumps(serialized_results.get('ticket_analyzer', {}), indent=2)}

2. HISTORY ANALYST AGENT RESULT:
{json.dumps(serialized_results.get('history_analyst', {}), indent=2)}

3. SKILL MATCHER AGENT RESULT:
{json.dumps(serialized_results.get('skill_matcher', {}), indent=2)}

4. AVAILABILITY CHECKER AGENT RESULT:
{json.dumps(serialized_results.get('availability_checker', {}), indent=2)}

5. POLICY CHECKER AGENT RESULT:
{json.dumps(serialized_results.get('policy_checker', {}), indent=2)}

INSTRUCTIONS:
1. Carefully analyze each agent's findings
2. Consider the following factors in your decision:
   - Skill match and proficiency level
   - Historical performance and success rate
   - Current availability and workload
   - Policy compliance and risk factors
   - Ticket complexity and urgency
   
3. Provide your recommendation in the following JSON format:
{{
    "recommended_employee": "Employee Name or ID",
    "confidence_score": 0.95,
    "reasoning": {{
        "primary_factors": ["List of main reasons for this choice"],
        "skill_analysis": "Why this employee's skills match best",
        "availability_analysis": "Analysis of availability and workload",
        "risk_assessment": "Any risks or concerns identified",
        "alternative_options": "Brief mention of other viable candidates if any"
    }},
    "assignment_recommendations": {{
        "estimated_completion_time": "X hours/days",
        "success_probability": 0.90,
        "monitoring_points": ["Key areas to monitor during assignment"],
        "support_needed": ["Any additional support or resources needed"]
    }}
}}

4. If no employee is suitable, recommend "NONE" and explain why in the reasoning.
5. Be thorough but concise in your analysis.
6. Consider both technical and soft factors in your decision.

RECOMMENDATION:
"""
        
        # Generate response from Gemini
        print("🧠 Sending agent results to Gemini API for final recommendation...")
        response = model.generate_content(prompt)
        response_text = response.text
        
        print(f"🤖 Gemini API Response: {response_text[:200]}...")
        
        # Try to parse JSON response
        try:
            # Extract JSON from response (in case there's additional text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                recommendation = json.loads(json_str)
            else:
                # If no JSON found, create structured response from text
                recommendation = {
                    "recommended_employee": "PARSING_ERROR",
                    "confidence_score": 0.0,
                    "reasoning": {
                        "primary_factors": ["Could not parse structured response"],
                        "skill_analysis": "Response parsing failed",
                        "availability_analysis": "Response parsing failed",
                        "risk_assessment": "Response parsing failed",
                        "alternative_options": "Response parsing failed"
                    },
                    "raw_response": response_text
                }
        
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            # Create fallback response
            recommendation = {
                "recommended_employee": "PARSING_ERROR",
                "confidence_score": 0.0,
                "reasoning": {
                    "primary_factors": ["JSON parsing failed"],
                    "skill_analysis": "Could not parse Gemini response",
                    "availability_analysis": "Could not parse Gemini response", 
                    "risk_assessment": "Could not parse Gemini response",
                    "alternative_options": "Could not parse Gemini response"
                },
                "raw_response": response_text,
                "error": str(e)
            }
        
        return {
            "success": True,
            "recommendation": recommendation,
            "ticket_id": ticket_info.get('id', 'N/A'),
            "serialized_agent_results": serialized_results  # Include for debugging
        }
        
    except Exception as e:
        print(f"❌ Error in get_final_employee_recommendation: {e}")
        return {
            "success": False,
            "error": str(e),
            "ticket_id": ticket_info.get('id', 'N/A')
        }


def get_and_return_agents(tkt_name, tkt_id, description, required_skills, suggested_employee, priority, due_date, exist_skills):
    tkt_obj = TicketAnalyzerAgents()
    his_obj = HistoryAnalyst()
    avl_obj =  AvailabilityCheckerAgent()
    policy_obj = PolicyChecker()

    emp_db_path = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employee_with_ids.xlsx"
    leave_db_path = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\Final_Employees_Leave_Table.xlsx"
    col_name = "name"

    
    # Build employee profiles
    employee_profiles = build_employee_profiles(
        employee_names=suggested_employee,
        excel_path=emp_db_path,
        leave_db_path=leave_db_path,
        name_column=col_name,
        designation_column="job_title",
        default_department="Development"
    )

    print("1️⃣ Running Ticket Analyzer Agent...")
    agent_1_res = tkt_obj.analyze_with_agent_system(required_skills, description, exist_skills)
    
    print("2️⃣ Running History Analyst Agent...")
    rep_agent_1 = his_obj.analyze_employee_for_ticket(tkt_name, description, required_skills, suggested_employee)
    agent_2_res = his_obj.analyze_with_agent_system(tkt_name, description, required_skills, suggested_employee)
    
    print("3️⃣ Running Skill Matcher Agent...")
    normalize_skills(required_skills)
    agent_3_res = fetch_employee_profiles(suggested_employee, emp_db_path)

    print("4️⃣ Running Availability Checker Agent...")
    agent_4_res = avl_obj.check_with_agent_system(suggested_employee, leave_db_path, emp_db_path)
    
    print("5️⃣ Running Policy Checker Agent...")
    # rep_agent_2 = policy_obj.analyze_hr_policy(tkt_name, tkt_id, description, employee_profiles, emp_db_path, col_name) 
    agent_5_res = policy_obj.analyze_with_agent_system(tkt_name, tkt_id, description, employee_profiles, emp_db_path, col_name)
    rep_agent_2 = policy_obj.analyze_hr_policy(tkt_name, tkt_id, description, employee_profiles, emp_db_path, col_name)

    agent_results = {
        "ticket_analyzer": agent_1_res,
        "history_analyst": agent_2_res,
        "skill_matcher": agent_3_res,
        "availability_checker": agent_4_res,
        "policy_checker": agent_5_res
    }
    
    # Compile ticket information
    ticket_info = {
        "name": tkt_name,
        "id": tkt_id,
        "description": description,
        "required_skills": required_skills,
        "suggested_employees": suggested_employee,
        "priority": priority,
        "due_date": due_date,
        "existing_skills": exist_skills
    }
    
    print("6️⃣ Getting final recommendation from Gemini...")
    # Get final recommendation from Gemini
    final_recommendation = get_final_employee_recommendation(agent_results, ticket_info)
    
    # Generate and save HTML report
    print("📄 Generating HTML report...")
    print("📄 Generating HTML report...")
    html_content = generate_html(final_recommendation, ticket_info)
    report_path = save_html_report_fixed_location(html_content)
    
    # Print results with better formatting
    print("\n" + "="*60)
    print("📋 AGENT ANALYSIS RESULTS:")
    print("="*60)
    
    # Print serialized results for better readability
    if final_recommendation.get("success") and "serialized_agent_results" in final_recommendation:
        serialized = final_recommendation["serialized_agent_results"]
        for i, (agent_name, result) in enumerate(serialized.items(), 1):
            print(f"{i}. {agent_name.replace('_', ' ').title()}: {str(result)[:100]}...")
    else:
        print(f"1. Ticket Analyzer: {str(agent_1_res)[:100]}...")
        print(f"2. History Analyst: {str(agent_2_res)[:100]}...")
        print(f"3. Skill Matcher: {str(agent_3_res)[:100]}...")
        print(f"4. Availability Checker: {str(agent_4_res)[:100]}...")
        print(f"5. Policy Checker: {str(agent_5_res)[:100]}...")
    
    print("\n" + "="*60)
    print("🎯 FINAL RECOMMENDATION:")
    print("="*60)
    
    if final_recommendation["success"]:
        recommendation = final_recommendation["recommendation"]
        print(f"👤 Recommended Employee: {recommendation.get('recommended_employee', 'N/A')}")
        print(f"📊 Confidence Score: {recommendation.get('confidence_score', 0.0)}")
        
        if 'reasoning' in recommendation:
            reasoning = recommendation['reasoning']
            print(f"💡 Primary Factors: {reasoning.get('primary_factors', [])}")
            print(f"🔧 Skill Analysis: {reasoning.get('skill_analysis', 'N/A')}")
            print(f"📅 Availability Analysis: {reasoning.get('availability_analysis', 'N/A')}")
            print(f"⚠️  Risk Assessment: {reasoning.get('risk_assessment', 'N/A')}")
        
        if 'assignment_recommendations' in recommendation:
            assign_rec = recommendation['assignment_recommendations']
            print(f"⏱️  Estimated Completion: {assign_rec.get('estimated_completion_time', 'N/A')}")
            print(f"✅ Success Probability: {assign_rec.get('success_probability', 0.0)}")
    else:
        print(f"❌ Error: {final_recommendation.get('error', 'Unknown error')}")
    
    if report_path:
        print(f"\n📄 HTML Report saved: {report_path}")
    
    return final_recommendation

def encode_html_to_base64(file_path: str) -> str:
    """
    Read HTML file and encode it to base64
    
    Args:
        file_path: Path to the HTML file
        
    Returns:
        Base64 encoded string of the HTML content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Encode to base64
        encoded_bytes = base64.b64encode(html_content.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error encoding {file_path} to base64: {e}")
        return None

def get_html_reports_as_base64(reports_folder: str) -> dict:
    """
    Get all HTML reports from the folder and return as base64 encoded strings
    
    Args:
        reports_folder: Path to the reports folder
        
    Returns:
        Dictionary with report names as keys and base64 encoded HTML as values
    """
    reports_folder = Path(reports_folder)
    
    # Define the expected report files
    report_files = {
        "policy_report": "policy_agent_report.html",
        "history_report": "history_report.html", 
        "availability_report": "availability_agent_report.html",
        "scorer_report": "scorer_agent_report.html",
        "summary_report": "summary_report.html"
    }
    
    base64_reports = {}
    
    for report_key, filename in report_files.items():
        file_path = reports_folder / filename
        
        if file_path.exists():
            encoded_content = encode_html_to_base64(str(file_path))
            if encoded_content:
                base64_reports[report_key] = encoded_content
            else:
                base64_reports[report_key] = None
                print(f"Warning: Could not encode {filename}")
        else:
            base64_reports[report_key] = None
            print(f"Warning: {filename} not found in {reports_folder}")
    
    return base64_reports

# def main(input_json):
#     tkt_name = input_json.get("ticket_name", None)
#     tkt_id = input_json.get("ticket_id", None)
#     description = input_json.get("description", None)
#     required_skills = input_json.get("required_skills", None)
#     suggested_employee = input_json.get("suggested_employee", None)
#     priority = input_json.get("priority", None)
#     due_date = input_json.get("due_date", None)
#     existing_skills = input_json.get("existing_skills", None)
    
#     final_recommendation = get_and_return_agents(tkt_name, tkt_id, description, required_skills, suggested_employee, priority, due_date, existing_skills)
#     return final_recommendation  # Return the actual recommendation instead of just "completed"


def main_alternative(input_json):

    if "llm_input" in input_json:
        value = input_json.get("llm_input")
        chat_main(value)

        with open("ex_json.json", "r") as f:
            data = json.load(f)

        tkt_name_llm = data.get("ticket_number")
        description_llm = data.get("description")
        suggested_employee_llm = data.get("assignee")
        priority_llm = data.get("priority")
        status__llm = data.get("status")
        required_skills_llm = data.get("skill_set")

        # Get the recommendation from your existing function
        final_recommendation = get_and_return_agents(tkt_name_llm, tkt_id, description_llm, required_skills_llm, suggested_employee_llm, priority_llm, due_date, existing_skills)
        
        # Path to your reports folder
        reports_folder = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec"
        
        # Get all HTML reports as base64
        html_reports_base64 = get_html_reports_as_base64(reports_folder)
        
        # Create the final response with reports at top level
        response = {
            "status": "success",
            "recommendation": final_recommendation,
            "policy_report": html_reports_base64.get("policy_report"),
            "history_report": html_reports_base64.get("history_report"),
            "availability_report": html_reports_base64.get("availability_report"),
            "scorer_report": html_reports_base64.get("scorer_report"),
            "summary_report": html_reports_base64.get("summary_report")
        }
        
        return response

    else:
        tkt_name = input_json.get("ticket_name", None)
        tkt_id = input_json.get("ticket_id", None)
        description = input_json.get("description", None)
        required_skills = input_json.get("required_skills", None)
        suggested_employee = input_json.get("suggested_employee", None)
        priority = input_json.get("priority", None)
        due_date = input_json.get("due_date", None)
        existing_skills = input_json.get("existing_skills", None)
        
        # Get the recommendation from your existing function
        final_recommendation = get_and_return_agents(tkt_name, tkt_id, description, required_skills, suggested_employee, priority, due_date, existing_skills)
        
        # Path to your reports folder
        reports_folder = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec"
        
        # Get all HTML reports as base64
        html_reports_base64 = get_html_reports_as_base64(reports_folder)
        
        # Create the final response with reports at top level
        response = {
            "status": "success",
            "recommendation": final_recommendation,
            "policy_report": html_reports_base64.get("policy_report"),
            "history_report": html_reports_base64.get("history_report"),
            "availability_report": html_reports_base64.get("availability_report"),
            "scorer_report": html_reports_base64.get("scorer_report"),
            "summary_report": html_reports_base64.get("summary_report")
        }
        
        return response


if __name__ == "__main__":
    # Example usage with sample data
    sample_input = {
        "ticket_name": "Sample Ticket",
        "ticket_id": "TKT-001",
        "description": "Sample ticket description",
        "required_skills": ["Python", "Machine Learning"],
        "suggested_employee": ["John Doe", "Jane Smith"],
        "priority": "High",
        "due_date": "2025-07-25",
        "existing_skills": ["Python", "Data Analysis"]
    }
    
    result = main_alternative(sample_input)
    print(f"\n🎉 Analysis completed! Result: {result.get('success', False)}")