from crewai import Agent
from crewai.tools import BaseTool
from dotenv import load_dotenv
from typing import Type
from pydantic import BaseModel, Field

# Import your existing tool implementations
from tools.fetch_emp_profile_tool import fetch_employee_profiles
from tools.get_emp_history_tool import get_employee_history
from tools.calc_similarity_tool import calculate_similarity
from tools.enrich_skill_tool import enrich_skills_with_llm
from tools.normalize_skills_tools import normalize_skills
from tools.check_avl_tool import check_availability
from tools.rag_policy_check import rag_policy_checker
from tools.score_employees_tool import score_employees
from tools.log_assignment_tool import log_assignment

load_dotenv()

# Define input schemas for your tools
class EnrichSkillsInput(BaseModel):
    """Input schema for enrich skills tool."""
    description: str = Field(..., description="The ticket description to analyze")
    existing_skills: list = Field(default=[], description="List of existing skills if any")

class NormalizeSkillsInput(BaseModel):
    """Input schema for normalize skills tool."""
    skills: list = Field(..., description="List of skills to normalize")

class GetEmployeeHistoryInput(BaseModel):
    """Input schema for get employee history tool."""
    employee_id: str = Field(..., description="Employee ID to get history for")

class CalculateSimilarityInput(BaseModel):
    """Input schema for calculate similarity tool."""
    current_ticket: str = Field(..., description="Current ticket description")
    historical_tickets: list = Field(..., description="List of historical tickets")

class FetchEmployeeProfilesInput(BaseModel):
    """Input schema for fetch employee profiles tool."""
    employee_ids: list = Field(..., description="List of employee IDs to fetch profiles for")

class CheckAvailabilityInput(BaseModel):
    """Input schema for check availability tool."""
    employee_id: str = Field(..., description="Employee ID to check availability for")
    start_date: str = Field(..., description="Start date for availability check")
    end_date: str = Field(..., description="End date for availability check")

class ScoreEmployeesInput(BaseModel):
    """Input schema for score employees tool."""
    ticket_name: str = Field(..., description="Name of the ticket")
    ticket_description: str = Field(..., description="Description of the ticket")
    employees_selected: list = Field(..., description="List of selected employees")
    ticket_analyzer_result: dict = Field(..., description="Result from ticket analyzer")
    history_analyst_result: dict = Field(..., description="Result from history analyst")
    skill_matcher_result: dict = Field(..., description="Result from skill matcher")
    availability_checker_result: dict = Field(..., description="Result from availability checker")
    policy_checker: dict = Field(..., description="Result from policy checker")

class LogAssignmentInput(BaseModel):
    """Input schema for log assignment tool."""
    ticket_name: str = Field(..., description="Name of the ticket")
    ticket_description: str = Field(..., description="Description of the ticket")
    selected_employee: str = Field(..., description="Name of selected employee")
    assignment_reason: str = Field(..., description="Reason for assignment")
    skill_match_score: float = Field(..., description="Skill match score")
    availability_score: float = Field(..., description="Availability score")
    experience_score: float = Field(..., description="Experience score")
    policy_compliance: bool = Field(..., description="Policy compliance check")
    final_score: float = Field(..., description="Final weighted score")

# Create CrewAI-compatible tools by wrapping your existing functions
class EnrichSkillsWithLLMTool(BaseTool):
    name: str = "enrich_skills_with_llm"
    description: str = "Analyze ticket description and enrich skills with LLM"
    args_schema: Type[BaseModel] = EnrichSkillsInput
    
    def _run(self, description: str, existing_skills: list = None) -> str:
        try:
            # Call your existing function
            result = enrich_skills_with_llm(description, existing_skills or [])
            return str(result)
        except Exception as e:
            return f"Error enriching skills: {str(e)}"

class NormalizeSkillsTool(BaseTool):
    name: str = "normalize_skills"
    description: str = "Normalize and standardize skills list"
    args_schema: Type[BaseModel] = NormalizeSkillsInput
    
    def _run(self, skills: list) -> str:
        try:
            result = normalize_skills(skills)
            return str(result)
        except Exception as e:
            return f"Error normalizing skills: {str(e)}"

class GetEmployeeHistoryTool(BaseTool):
    name: str = "get_employee_history"
    description: str = "Get employee ticket history"
    args_schema: Type[BaseModel] = GetEmployeeHistoryInput
    
    def _run(self, employee_id: str) -> str:
        try:
            result = get_employee_history(employee_id)
            return str(result)
        except Exception as e:
            return f"Error getting employee history: {str(e)}"

class CalculateSimilarityTool(BaseTool):
    name: str = "calculate_similarity"
    description: str = "Calculate similarity between current and historical tickets"
    args_schema: Type[BaseModel] = CalculateSimilarityInput
    
    def _run(self, current_ticket: str, historical_tickets: list) -> str:
        try:
            result = calculate_similarity(current_ticket, historical_tickets)
            return str(result)
        except Exception as e:
            return f"Error calculating similarity: {str(e)}"

class FetchEmployeeProfilesTool(BaseTool):
    name: str = "fetch_employee_profiles"
    description: str = "Fetch employee profiles from HRMS"
    args_schema: Type[BaseModel] = FetchEmployeeProfilesInput
    
    def _run(self, employee_ids: list) -> str:
        try:
            result = fetch_employee_profiles(employee_ids)
            return str(result)
        except Exception as e:
            return f"Error fetching employee profiles: {str(e)}"

class CheckAvailabilityTool(BaseTool):
    name: str = "check_availability"
    description: str = "Check employee availability"
    args_schema: Type[BaseModel] = CheckAvailabilityInput
    
    def _run(self, employee_id: str, start_date: str, end_date: str) -> str:
        try:
            result = check_availability(employee_id, start_date, end_date)
            return str(result)
        except Exception as e:
            return f"Error checking availability: {str(e)}"

class ScoreEmployeesTool(BaseTool):
    name: str = "score_employees"
    description: str = "Score employees based on various criteria"
    args_schema: Type[BaseModel] = ScoreEmployeesInput
    
    def _run(self, ticket_name: str, ticket_description: str, employees_selected: list, 
             ticket_analyzer_result: dict, history_analyst_result: dict, 
             skill_matcher_result: dict, availability_checker_result: dict, 
             policy_checker: dict) -> str:
        try:
            result = score_employees(
                ticket_name, ticket_description, employees_selected,
                ticket_analyzer_result, history_analyst_result, 
                skill_matcher_result, availability_checker_result, policy_checker
            )
            return str(result)
        except Exception as e:
            return f"Error scoring employees: {str(e)}"

class LogAssignmentTool(BaseTool):
    name: str = "log_assignment"
    description: str = "Log the final assignment decision"
    args_schema: Type[BaseModel] = LogAssignmentInput
    
    def _run(self, ticket_name: str, ticket_description: str, selected_employee: str,
             assignment_reason: str, skill_match_score: float, availability_score: float,
             experience_score: float, policy_compliance: bool, final_score: float) -> str:
        try:
            result = log_assignment(
                ticket_name, ticket_description, selected_employee,
                assignment_reason, skill_match_score, availability_score,
                experience_score, policy_compliance, final_score
            )
            return str(result)
        except Exception as e:
            return f"Error logging assignment: {str(e)}"

# Create a custom RAG policy checker tool
class RagPolicyCheckerTool(BaseTool):
    name: str = "rag_policy_checker"
    description: str = "Check HR policy compliance using RAG"
    
    def __init__(self, tkt_name: str, tkt_id: str, tkt_description: str, 
                 emp_profile: dict, excel_path: str, col_name: str):
        super().__init__()
        self.tkt_name = tkt_name
        self.tkt_id = tkt_id
        self.tkt_description = tkt_description
        self.emp_profile = emp_profile
        self.excel_path = excel_path
        self.col_name = col_name
    
    def _run(self, query: str = "") -> str:
        try:
            # Call your existing RAG policy checker
            result = rag_policy_checker(
                self.tkt_name, self.tkt_id, self.tkt_description,
                self.emp_profile, self.excel_path, self.col_name
            )
            return str(result)
        except Exception as e:
            return f"Error checking policy: {str(e)}"

class TicketAnalyzerAgents:
    def ticket_analyzer(self, skills, description):
        print("````````Entered Ticket Analyzer Agent``````````")
        return Agent(
            role='Ticket Understanding & Skill Extraction',
            goal='Analyze the ticket content and extract required skills and type of task.',
            backstory="""You are a seasoned product analyst who has worked across hundreds of agile teams.
                        Your instinct for understanding unclear requirements and transforming them into clear, actionable insights is unmatched. 
                        You specialize in dissecting ticket descriptions to identify what needs to be done and which skills are required — even if the request is vague or missing details. 
                        Your job is to ensure no ambiguity exists before the ticket goes into the system.
                      """,
            description="""
                        You are responsible for deeply analyzing the ticket information provided by the manager.
                        Your job is to classify the ticket into a type: bug, feature request, enhancement, or support.
                        Based on the ticket description, extract and suggest the required technical skills (e.g., LWC, JS).
                        If the manager has already provided skills, you should verify and enrich them with relevant alternatives.
                        Output a clean summary including task type and validated skill list.
                        
                        Follow this process:
                        1. First use enrich_skills_with_llm to analyze the ticket description and get additional skills
                            - Pass the ticket description and any existing skills
                        2. Then use normalize_skills to standardize all the skills from step 1
                        3. Classify the ticket type (bug, feature request, enhancement, or support)
                        4. Provide a final summary with ticket type and normalized skills
                        """,
            tools=[EnrichSkillsWithLLMTool(), NormalizeSkillsTool()],
            allow_delegation=True,
            verbose=True
        )
    
    def history_analyst(self, emp_list, description, skills, ticket_name):
        return Agent(
            role='Employee Ticket History Evaluator',
            goal='Score employees based on their similarity with past resolved tickets.',
            backstory="""You are the company's internal historian — an expert at spotting patterns in project history.
                        You've reviewed thousands of past tickets and know exactly which employees shine in which kinds of tasks.
                        You use this wisdom to match the right person to the right task based on what they've solved before.
                      """,
            description="""
                        Your job is to evaluate the past performance of each employee in handling tickets similar to the current one.
                        You will access past tickets assigned to them, and compare based on task type, tags, and resolution success.
                        Return a relevance score or ranking showing how well each employee has handled similar tasks previously.
                        This helps determine who has the most experience with this kind of problem.
                        """,
            tools=[GetEmployeeHistoryTool(), CalculateSimilarityTool()],
            allow_delegation=True,
            verbose=True
        )
    
    def skill_matcher(self, emp_list):
        return Agent(
            role='Skill-to-Employee Matcher',
            goal='Match required skills from the ticket with employee profiles.',
            backstory="""You are the organization's tech talent scout.
                        Your strength lies in deeply understanding both the technical requirements of the ticket and the hidden strengths of each employee.
                        You think like a recruiter and a tech lead rolled into one — quickly zeroing in on who has the skills and experience to deliver.
                        Your decisions are based on data from HRMS, certifications, and project exposure.
                      """,
            description="""
                        You are responsible for matching the ticket's required skills to the available employee pool.
                        Use HRMS data such as listed skills, certifications, years of experience, and technology stacks.
                        Prioritize employees who meet most or all required skills and have experience in the project's domain.
                        Output a ranked list of employees with a short reasoning per match."
                        """,
            tools=[FetchEmployeeProfilesTool(), NormalizeSkillsTool()],
            allow_delegation=True,
            verbose=True
        )
    
    def availability(self):
        return Agent(
            role='Employee Availability Checker',
            goal='Filter out employees who are currently unavailable or overbooked',
            backstory="""You are a timekeeper and workload balancer.
                        You live inside the HRMS and calendars, and you're obsessed with efficiency.
                        Before assigning any task, you make sure employees are not on leave, overloaded, or already committed. 
                        You ensure fair distribution and timely delivery by maintaining real-world feasibility.
                      """,
            description="""
                        You check each candidate's current workload, leave status, and calendar availability using HRMS data.
                        Exclude any employee who is on leave, has overlapping tasks, or can't complete the task in the requested timeframe.
                        Ensure only available employees are forwarded to the next step.
                      """,
            tools=[CheckAvailabilityTool()],
            allow_delegation=True,
            verbose=True
        )

    def policy_checker(self, tkt_name, tkt_id, tkt_description, emp_profile, excel_path, col_name):
        return Agent(
            role='HR Policy Compliance Validator',
            goal='Ensure the assignment adheres to internal company policies.',
            backstory="""You are the digital guardian of HR policy. 
                        You've memorized every internal rule, exception, and sensitive domain restriction.
                        You operate through a powerful RAG system that lets you recall the right rule at the right time. 
                        Your mission is to ensure every assignment is not only optimal — but also compliant, secure, and ethical.
                      """,
            description="""
                        You act as a gatekeeper to verify task assignments follow HR rules.
                        Use a RAG-based system to retrieve and apply policies from internal documents (e.g., interns can't work on finance projects).
                        Validate if the selected employees are allowed to handle this ticket based on department, project, or access level.
                        Return filtered results and highlight any violations detected.
                      """,
            tools=[RagPolicyCheckerTool(tkt_name, tkt_id, tkt_description, emp_profile, excel_path, col_name)],
            allow_delegation=True,
            verbose=True
        )

    def assignment_coordinator(self, ticket_name, ticket_description, employees_selected):
        return Agent(
            role='Final Assignment Decision-Maker',
            goal='Choose the most suitable employee for the ticket and log the final assignment.',
            backstory="""You are the orchestrator — a wise, fair, and balanced decision-maker. 
                        After hearing input from all the specialists (skill matcher, availability checker, policy reviewer, etc.), you synthesize the insights. 
                        You weigh trade-offs, resolve conflicts, and make the final call on who gets the job. 
                        You're known for always backing your decisions with clear, rational reasoning and proper documentation.
                      """,
            description=f"""
                            You receive candidate recommendations and filtered scores from the other agents. 
                            Make the final decision on which employee should be assigned the task. 
                            Balance skill match, availability, past experience, and policy constraints.
                            
                            WORKFLOW:
                            1. Use score_employees tool to evaluate all candidates
                            2. Select the best employee based on the scoring results
                            3. Use log_assignment tool to officially record the assignment
                            
                            Required inputs for score_employees:
                            - ticket_name: {ticket_name}
                            - ticket_description: {ticket_description}
                            - employees_selected: {employees_selected}
                            - ticket_analyzer_result: (from previous agent)
                            - history_analyst_result: (from previous agent)
                            - skill_matcher_result: (from previous agent)
                            - availability_checker_result: (from previous agent)
                            - policy_checker: (from previous agent)
                            
                            Required inputs for log_assignment:
                            - ticket_name: The ticket being assigned
                            - ticket_description: Full ticket description
                            - selected_employee: Name of chosen employee
                            - assignment_reason: Detailed explanation of selection
                            - skill_match_score: Skill scoring result
                            - availability_score: Availability scoring result
                            - experience_score: Experience scoring result
                            - policy_compliance: Policy compliance check result
                            - final_score: Overall weighted score
                            
                            Always complete both steps: scoring and logging the assignment.
                          """,
            tools=[ScoreEmployeesTool(), LogAssignmentTool()],
            allow_delegation=True,
            verbose=True
        )