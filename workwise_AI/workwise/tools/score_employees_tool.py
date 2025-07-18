from langchain.tools import tool
import google.generativeai as genai
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API with error handling
def configure_gemini():
    """Configure Gemini API with proper error handling"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    if not api_key.startswith('AIza'):
        raise ValueError("Invalid API key format. Make sure you're using a Google AI Studio API key")
    
    genai.configure(api_key=api_key)
    return api_key

@tool
def score_employees(ticket_name: str, ticket_description: str, employees_selected: list, 
                   ticket_analyzer_result, history_analyst_result, skill_matcher_result, 
                   availability_checker_result, policy_checker) -> list:
    """
    Scores employees based on comprehensive analysis from multiple agents using Gemini AI.
    Returns a list of employees with detailed scores and reasoning.
    """
    
    # System prompt explaining each agent's role
    system_prompt = """
    You are an AI Employee Scoring Agent for a ticketing system. Your task is to analyze results from multiple specialized agents and provide a comprehensive score (0-100) for each employee's suitability for a given ticket.

    AGENT DESCRIPTIONS:
    
    1. TICKET_ANALYZER_RESULT: Analyzes the ticket content, extracts key requirements, technologies, complexity level, and priority. Provides insights into what skills and experience are needed.
    
    2. HISTORY_ANALYST_RESULT: Examines each employee's past ticket history, performance metrics, success rates, average resolution times, and expertise areas based on previous work.
    
    3. SKILL_MATCHER_RESULT: Compares required skills from the ticket against each employee's skill set, providing skill match percentages and identifying skill gaps.
    
    4. AVAILABILITY_CHECKER_RESULT: Checks if employees are currently available or on leave, provides availability status and return dates if unavailable.
    
    5. POLICY_CHECKER: Validates against company policies, work regulations, compliance requirements, and any restrictions for ticket assignment.

    SCORING CRITERIA:
    - Technical Skills Match (25%): How well the employee's skills align with ticket requirements
    - Experience & History (25%): Past performance on similar tickets, success rate, resolution time
    - Availability (20%): Current availability status, workload capacity
    - Policy Compliance (15%): Adherence to company policies and assignment rules
    - Overall Suitability (15%): General fit considering all factors

    SCORING SCALE:
    - 90-100: Excellent match, highly recommended
    - 80-89: Very good match, recommended
    - 70-79: Good match, suitable
    - 60-69: Fair match, acceptable with considerations
    - 50-59: Poor match, not recommended
    - 0-49: Very poor match, should not be assigned

    OUTPUT FORMAT:
    Return a JSON array with employee scores in this exact format:
    [
        {
            "employee_name": "Employee Name",
            "overall_score": 85,
            "skill_match_score": 90,
            "experience_score": 80,
            "availability_score": 100,
            "policy_score": 95,
            "recommendation": "Highly recommended",
            "reasoning": "Detailed explanation of scoring rationale",
            "strengths": ["List of key strengths"],
            "concerns": ["List of any concerns or limitations"]
        }
    ]
    """
    
    # Prepare the analysis prompt
    analysis_prompt = f"""
    TICKET INFORMATION:
    Ticket Name: {ticket_name}
    Ticket Description: {ticket_description}
    Employees to Score: {employees_selected}
    
    AGENT RESULTS:
    
    Ticket Analyzer Result:
    {json.dumps(ticket_analyzer_result, indent=2)}
    
    History Analyst Result:
    {json.dumps(history_analyst_result, indent=2)}
    
    Skill Matcher Result:
    {json.dumps(skill_matcher_result, indent=2)}
    
    Availability Checker Result:
    {json.dumps(availability_checker_result, indent=2)}
    
    Policy Checker Result:
    {json.dumps(policy_checker, indent=2)}
    
    Please analyze all the above information and provide comprehensive scores for each employee. Consider all factors and provide detailed reasoning for your scoring decisions.
    """
    
    try:
        # Configure Gemini API
        configure_gemini()
        
        # Initialize Gemini model with specific configuration
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config=genai.GenerationConfig(
                temperature=0.1,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
            )
        )
        
        # Generate response
        response = model.generate_content([system_prompt, analysis_prompt])
        
        # Check if response was blocked
        if response.prompt_feedback.block_reason:
            print(f"Response blocked: {response.prompt_feedback.block_reason}")
            raise Exception(f"Content was blocked: {response.prompt_feedback.block_reason}")
        
        # Parse the response
        response_text = response.text
        
        # Extract JSON from response (handle potential markdown formatting)
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "[" in response_text and "]" in response_text:
            json_start = response_text.find("[")
            json_end = response_text.rfind("]") + 1
            json_text = response_text[json_start:json_end]
        else:
            json_text = response_text
        
        # Parse JSON
        try:
            scored_employees = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            # Fallback: create basic structure if JSON parsing fails
            scored_employees = []
            for employee in employees_selected:
                scored_employees.append({
                    "employee_name": employee,
                    "overall_score": 50,
                    "skill_match_score": 50,
                    "experience_score": 50,
                    "availability_score": 50,
                    "policy_score": 50,
                    "recommendation": "Unable to analyze",
                    "reasoning": "Error in processing agent results",
                    "strengths": ["Analysis incomplete"],
                    "concerns": ["Unable to evaluate properly"]
                })
        
        # Sort by overall score (highest first)
        scored_employees.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
        
        return scored_employees
        
    except Exception as e:
        print(f"Error in scoring employees: {str(e)}")
        print(f"Error type: {type(e)}")
        
        # Return fallback scores
        fallback_scores = []
        for employee in employees_selected:
            fallback_scores.append({
                "employee_name": employee,
                "overall_score": 50,
                "skill_match_score": 50,
                "experience_score": 50,
                "availability_score": 50,
                "policy_score": 50,
                "recommendation": "Analysis failed",
                "reasoning": f"Error occurred during scoring: {str(e)}",
                "strengths": ["Unable to determine"],
                "concerns": ["Scoring system unavailable"]
            })
        
        return fallback_scores


if __name__ == "__main__":
    # Debug environment variables
    print("=== Debug Info ===")
    print(f"Current directory: {os.getcwd()}")
    
    # Test the configuration first
    try:
        api_key = configure_gemini()
        print(f"✓ API Key configured successfully")
        print(f"✓ API Key length: {len(api_key)}")
        
        # Test with a simple prompt first
        model = genai.GenerativeModel('gemini-1.5-flash')
        test_response = model.generate_content("Hello, respond with just 'OK'")
        print(f"✓ Test response: {test_response.text}")
        
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        print(f"✗ Error type: {type(e)}")
        exit(1)
    
    # Sample test data
    ticket_name = "LWC Issue"
    description = "Fix button layout issues and apply responsive design in LWC component."
    employees = ["Mark Jenkins", "Kenneth Simpson", "Anthony Wright"]
    
    # Sample agent results (you would replace these with actual results)
    ticket_analyzer_result = {"complexity": "medium", "technologies": ["LWC", "CSS", "JavaScript"], "priority": "high"}
    history_analyst_result = {"Mark Jenkins": {"success_rate": 85, "avg_resolution_time": 2.5}, "Kenneth Simpson": {"success_rate": 90, "avg_resolution_time": 2.0}}
    skill_matcher_result = {"Mark Jenkins": {"skill_match": 85}, "Kenneth Simpson": {"skill_match": 92}}
    availability_checker_result = [{"employee_name": "Mark Jenkins", "status": "available"}, {"employee_name": "Kenneth Simpson", "status": "available"}]
    policy_checker = {"all_employees_compliant": True}
    
    # Test the scoring function
    results = score_employees.func(ticket_name, description, employees, ticket_analyzer_result, history_analyst_result, skill_matcher_result, availability_checker_result, policy_checker)
    
    for result in results:
        print(f"Employee: {result['employee_name']}, Score: {result['overall_score']}")