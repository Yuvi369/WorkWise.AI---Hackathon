import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from langchain.tools import tool
import json
from typing import List, Dict, Any

from tools.history_report import generate_html_report
# Load .env
load_dotenv()

# Load the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

@tool
def get_employee_history(employee_names: list = None, skills_list: list = None) -> list:
    """
    Fetches ticket history for given employee(s) from Excel files and scores them based on required skills.
    
    Args:
        employee_names: List of employee names to analyze
        skills_list: List of required skills to match against
    
    Returns:
        List of employee scores and skill analysis
    """
    
    try:
        # File paths (adjust these to your actual file paths)
        EMP_FILE_PATH = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_db.xlsx"  # Base employee file
        TKT_HISTORY_FILE_PATH = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\tkt_history_FS.xlsx"  # Ticket history file
        
        # Step 1: Load the employee base file
        print("📁 Loading employee base file...")
        try:
            emp_df = pd.read_excel(EMP_FILE_PATH)
            print(f"✅ Loaded {len(emp_df)} employees from base file")
        except FileNotFoundError:
            print(f"❌ Employee file not found: {EMP_FILE_PATH}")
            return []
        except Exception as e:
            print(f"❌ Error loading employee file: {e}")
            return []
        
        # Step 2: Load ticket history file (Sheet2)
        print("📁 Loading ticket history file (Sheet2)...")
        try:
            tkt_df = pd.read_excel(TKT_HISTORY_FILE_PATH, sheet_name=1)  # sheet_name=1 for Sheet2 (0-indexed)
            print(f"✅ Loaded {len(tkt_df)} ticket records from Sheet2")
        except FileNotFoundError:
            print(f"❌ Ticket history file not found: {TKT_HISTORY_FILE_PATH}")
            return []
        except Exception as e:
            print(f"❌ Error loading ticket history file: {e}")
            return []
        
        # Step 3: Initialize result list
        result_list = []
        
        # Get employee name column (adjust column name as needed)
        emp_name_col = 'employee_name' if 'employee_name' in emp_df.columns else emp_df.columns[0]
        tkt_emp_col = 'assigned_to' if 'assigned_to' in tkt_df.columns else 'employee_name'
        
        # print(f'***** {emp_name_col} *****')
        # Debug: Print column info
        print(f"📋 Employee file columns: {list(emp_df.columns)}")
        print(f"📋 Using employee column: '{emp_name_col}'")
        print(f"📋 Ticket file columns: {list(tkt_df.columns)}")
        print(f"📋 Using ticket column: '{tkt_emp_col}'")


        print(f"📋 First 5 employees in base file: {emp_df[emp_name_col].head().tolist()}")
        # Step 4: Process each employee
        for emp_name in employee_names:
            print(f"\n🔍 Processing employee: {emp_name}")

            emp_name_clean = emp_name.strip()
            base_employees = emp_df[emp_name_col].astype(str).str.strip()
            
            # Step 1: Check if employee exists in base file (case-insensitive)
            exact_match = emp_name_clean in base_employees.values
            case_insensitive_match = emp_name_clean.lower() in base_employees.str.lower().values
            
            if not exact_match and not case_insensitive_match:
                print(f"❌ Employee '{emp_name}' not found in base employee file")
                print(f"🔍 Searching for similar names...")
                
                # Try to find similar names
                similar_names = base_employees[base_employees.str.contains(emp_name_clean.split()[0], case=False, na=False)].head(3).tolist()
                if similar_names:
                    print(f"💡 Similar names found: {similar_names}")
                continue
            
            # Get the actual matched name from the base file
            if exact_match:
                matched_name = emp_name_clean
                print(f"✅ Employee '{emp_name}' found in base file (exact match)")
            else:
                matched_name = base_employees[base_employees.str.lower() == emp_name_clean.lower()].iloc[0]
                print(f"✅ Employee '{emp_name}' found in base file (case-insensitive match: '{matched_name}')")
            
            # Step 2: Check if employee has ticket history (use matched name)
            employee_tickets = tkt_df[tkt_df[tkt_emp_col].astype(str).str.strip().str.lower() == matched_name.lower()]
            
            # Step 1: Check if employee exists in base file
            # if emp_name not in emp_df[emp_name_col].values:
            #     print(f"❌ Employee '{emp_name}' not found in base employee file")
            #     continue
            
            # print(f"✅ Employee '{emp_name}' found in base file")
            
            # # Step 2: Check if employee has ticket history
            # employee_tickets = tkt_df[tkt_df[tkt_emp_col] == emp_name]
            
            if employee_tickets.empty:
                print(f"❌ No ticket history found for '{matched_name}'")
                # Try searching with original name as fallback
                employee_tickets = tkt_df[tkt_df[tkt_emp_col].astype(str).str.strip().str.lower() == emp_name_clean.lower()]
                if employee_tickets.empty:
                    print(f"❌ No ticket history found for '{emp_name}' either")
                    result_list.append({
                        'employee_name': emp_name,
                        'skills_extracted': [],
                        'ticket_count': 0,
                        'score': 0,
                        'message': 'No ticket history found'
                    })
                    continue
                else:
                    print(f"✅ Found {len(employee_tickets)} tickets using original name '{emp_name}'")
            else:
                print(f"✅ Found {len(employee_tickets)} tickets for '{matched_name}'")
            
            # Step 4: Extract skills from ticket history using Gemini
            ticket_data = []
            for _, ticket in employee_tickets.iterrows():
                ticket_info = {
                    'ticket_name': ticket.get('ticket_name', ''),
                    'description': ticket.get('description', ''),
                    'comments': ticket.get('comments', '')
                }
                ticket_data.append(ticket_info)
            
            # Call Gemini to extract skills
            extracted_skills = extract_skills_from_tickets(ticket_data, emp_name)
            
            # Store employee result
            result_list.append({
                'employee_name': emp_name,
                'skills_extracted': extracted_skills,
                'ticket_count': len(employee_tickets),
                'tickets_processed': ticket_data
            })
        
        # Step 6: Score employees based on required skills
        if skills_list and result_list:
            print(f"\n🎯 Scoring employees based on required skills: {skills_list}")
            scored_results = score_employees_with_gemini(result_list, skills_list)
            return scored_results
        else:
            return result_list
            
    except Exception as e:
        print(f"❌ Error in get_employee_history: {e}")
        return []

def extract_skills_from_tickets(ticket_data: List[Dict], employee_name: str) -> List[str]:
    """
    Use Gemini to extract skills from ticket data
    """
    try:
        # Prepare the prompt for Gemini
        tickets_text = ""
        for i, ticket in enumerate(ticket_data, 1):
            tickets_text += f"""
            Ticket {i}:
            Name: {ticket['ticket_name']}
            Description: {ticket['description']}
            Comments: {ticket['comments']}
            ---
            """
        
        prompt = f"""
        Analyze the following ticket history for employee '{employee_name}' and extract all technical skills, technologies, and competencies demonstrated:

        {tickets_text}

        IMPORTANT: You must respond with ONLY a valid JSON array of strings. No additional text, explanations, or formatting.
        
        Focus on extracting:
        - Programming languages (Python, JavaScript, Java, etc.)
        - Frameworks and libraries (React, Angular, Django, etc.)
        - Databases (MySQL, PostgreSQL, MongoDB, etc.)
        - Tools and technologies (Docker, Git, AWS, etc.)
        - Domain expertise (API development, Testing, etc.)
        - Soft skills (Problem-solving, Debugging, etc.)

        Example response format:
        ["Python", "React", "PostgreSQL", "Problem-solving"]
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        print(f"🔍 Raw response for {employee_name}: {response_text[:100]}...")
        
        # Try to extract JSON from response
        try:
            # Remove any markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            skills = json.loads(response_text)
            if isinstance(skills, list):
                print(f"✅ Extracted {len(skills)} skills for {employee_name}: {skills[:3]}...")
                return skills
            else:
                print(f"❌ Invalid response format for {employee_name}")
                return extract_skills_fallback(tickets_text, employee_name)
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error for {employee_name}: {e}")
            return extract_skills_fallback(tickets_text, employee_name)
            
    except Exception as e:
        print(f"❌ Error extracting skills for {employee_name}: {e}")
        return []

def extract_skills_fallback(tickets_text: str, employee_name: str) -> List[str]:
    """
    Fallback method to extract skills using a simpler approach
    """
    try:
        prompt = f"""
        Extract technical skills from this ticket history for {employee_name}:

        {tickets_text}

        List only the skills, one per line, no JSON format needed.
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse line by line
        skills = []
        for line in response_text.split('\n'):
            line = line.strip()
            if line and not line.startswith('-') and not line.startswith('*'):
                # Remove bullet points and numbering
                skill = line.replace('-', '').replace('*', '').replace('•', '').strip()
                if skill and len(skill) > 1:
                    skills.append(skill)
        
        print(f"✅ Fallback extracted {len(skills)} skills for {employee_name}")
        return skills[:10]  # Limit to top 10 skills
        
    except Exception as e:
        print(f"❌ Fallback extraction failed for {employee_name}: {e}")
        return []

def score_employees_with_gemini(employee_results: List[Dict], required_skills: List[str]) -> List[Dict]:
    """
    Use Gemini to score employees based on their skills vs required skills
    """
    try:
        # Prepare data for scoring
        employees_data = []
        for emp in employee_results:
            employees_data.append({
                'name': emp['employee_name'],
                'skills': emp['skills_extracted'],
                'ticket_count': emp['ticket_count']
            })
        
        prompt = f"""
        You are an HR analyst. Score the following employees based on how well their skills match the required skills.

        Required Skills: {required_skills}

        Employee Data:
        {json.dumps(employees_data, indent=2)}

        IMPORTANT: Respond with ONLY a valid JSON array. No additional text.

        For each employee, calculate a score from 0-100 based on skill match and provide this exact JSON format:
        [
            {{
                "employee_name": "Name",
                "score": 85,
                "matching_skills": ["skill1", "skill2"],
                "missing_skills": ["skill3"],
                "reasoning": "Brief explanation",
                "recommendation": "Strong Match/Good Match/Partial Match/Poor Match"
            }}
        ]
        """
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        print(f"🔍 Raw scoring response: {response_text[:200]}...")
        
        try:
            # Remove any markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            scores = json.loads(response_text)
            
            if isinstance(scores, list) and len(scores) > 0:
                # Merge scores with original data
                final_results = []
                for emp_result in employee_results:
                    emp_name = emp_result['employee_name']
                    
                    # Find corresponding score
                    score_data = next((s for s in scores if s['employee_name'] == emp_name), None)
                    
                    if score_data:
                        emp_result.update(score_data)
                    else:
                        # Fallback scoring
                        emp_result.update(score_employee_fallback(emp_result, required_skills))
                    
                    final_results.append(emp_result)
                
                # Sort by score (highest first)
                final_results.sort(key=lambda x: x.get('score', 0), reverse=True)
                
                print(f"✅ Successfully scored {len(final_results)} employees")
                return final_results
            else:
                print("❌ Invalid scoring response format")
                return score_employees_fallback(employee_results, required_skills)
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in scoring: {e}")
            return score_employees_fallback(employee_results, required_skills)
            
    except Exception as e:
        print(f"❌ Error scoring employees: {e}")
        return score_employees_fallback(employee_results, required_skills)

def score_employee_fallback(emp_result: Dict, required_skills: List[str]) -> Dict:
    """
    Fallback scoring method for individual employee
    """
    emp_skills = emp_result.get('skills_extracted', [])
    emp_skills_lower = [skill.lower() for skill in emp_skills]
    required_skills_lower = [skill.lower() for skill in required_skills]
    
    # Find matches
    matching_skills = []
    for req_skill in required_skills:
        for emp_skill in emp_skills:
            if req_skill.lower() in emp_skill.lower() or emp_skill.lower() in req_skill.lower():
                matching_skills.append(emp_skill)
                break
    
    # Calculate score
    if not required_skills:
        score = 0
    else:
        score = int((len(matching_skills) / len(required_skills)) * 100)
    
    # Missing skills
    missing_skills = [skill for skill in required_skills if skill not in [ms.lower() for ms in matching_skills]]
    
    # Recommendation
    if score >= 80:
        recommendation = "Strong Match"
    elif score >= 60:
        recommendation = "Good Match"
    elif score >= 40:
        recommendation = "Partial Match"
    else:
        recommendation = "Poor Match"
    
    return {
        'score': score,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'reasoning': f"Matched {len(matching_skills)}/{len(required_skills)} required skills",
        'recommendation': recommendation
    }

def score_employees_fallback(employee_results: List[Dict], required_skills: List[str]) -> List[Dict]:
    """
    Fallback scoring method for all employees
    """
    print("🔄 Using fallback scoring method...")
    
    for emp_result in employee_results:
        fallback_score = score_employee_fallback(emp_result, required_skills)
        emp_result.update(fallback_score)
    
    # Sort by score (highest first)
    employee_results.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    return employee_results

def print_results(results: List[Dict]):
    """
    Print formatted results
    """
    if not results:
        print("❌ No results to display")
        return
    
    print("\n" + "="*60)
    print("📊 EMPLOYEE ANALYSIS RESULTS")
    print("="*60)
    
    for i, emp in enumerate(results, 1):
        print(f"\n{i}. {emp['employee_name']}")
        print(f"   Score: {emp.get('score', 'N/A')}/100")
        print(f"   Tickets Processed: {emp.get('ticket_count', 0)}")
        
        if emp.get('matching_skills'):
            print(f"   ✅ Matching Skills: {', '.join(emp['matching_skills'])}")
        
        if emp.get('missing_skills'):
            print(f"   ❌ Missing Skills: {', '.join(emp['missing_skills'])}")
        
        if emp.get('reasoning'):
            print(f"   💡 Reasoning: {emp['reasoning']}")
        
        if emp.get('recommendation'):
            print(f"   🎯 Recommendation: {emp['recommendation']}")
        
        print("-" * 50)


# ✅ Test
if __name__ == "__main__":
    employee_profile = [
        "Mark Jenkins",
        "Kenneth Green", 
        "Amanda Lewis"
    ]

    skills_list = ['React', 'CSS', 'Production-deployment-experience', 'mongodb', 'bug-handling']

    print("🚀 Starting Employee History Analysis...")
    results = get_employee_history.func(employee_profile, skills_list)
    
    # Print formatted results
    print_results(results)
    
    # Generate HTML report
    if results:
        html_file = generate_html_report(results, skills_list)
        if html_file:
            print(f"🌐 Open the report in your browser: {html_file}")