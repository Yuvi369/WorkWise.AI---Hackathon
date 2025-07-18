from crewai import Task
from textwrap import dedent

class TicketAnalyzerTasks:

    def ticket_analyzer_task(self, agent
                            #skill_set, description
                            ):
        # additional_context = ""
        # if skill_set:
        #     additional_context += f"\n Required skills mentioned by the user to solve the ticket: {skill_set}"
        # if description:
        #     additional_context += f"\nDescription/Context for the ticket: {description}"
        return Task(
            description=dedent(f"""
                               
                You are a Ticket Analyzer Agent in an AI-powered workforce assignment system.

                Your task is to deeply analyze a new incoming ticket, understand the nature of the task (e.g., bug fix, feature request, performance issue), 
                and identify the **core technical skills required** to complete this task successfully.


                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                --- You must:
                1. Classify the type of ticket (e.g., bug, enhancement, performance, UI issue, etc.)
                2. Extract and normalize the technical skills required from the ticket description
                3. Include any relevant secondary skills if the description implies them
                4. Use the "Required skills mentioned by the user" as hints but not as the final list
                5. Ensure the output list is comprehensive and avoids duplicates

                --- Output format should include:
                - Ticket classification (1 line)
                - Normalized list of required skills (as a Python list)
                - Optional short explanation (2-3 lines) of how you inferred these skills

            """),
            agent=agent,
        )
    
    def history_analyst_task(self, agent):
        # additional_context = ""
        # if ticket_name:
        #     additional_context += f"\n Name of the ticket need to be assigned: {ticket_name}"
        # if ticked_id:
        #     additional_context += f"\n Ticket id: {ticked_id}"
        # if selected_employee:
        #     additional_context += f"\n Selected Employee for Evaluation: {selected_employee}"
      
        return Task(
            description=dedent(f"""
                               
                You are a History Analyst Agent in an AI-powered workforce management system.

                Your job is to evaluate whether the selected employee is a good fit for the ticket based on their past experience.

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                You will have access to the employee's historical ticket records including:
                - Titles, tags, and descriptions of previously completed tickets
                - Ticket outcomes and performance ratings (if available)
                - Skill domains used in past tickets

                🧠 Your analysis should answer:
                1. Has the employee worked on similar tickets before? If so, how often?
                2. Are the skills required for this ticket aligned with the employee’s past work?
                3. Was the employee successful in those tasks (if such metadata is available)?

                📝 Output format:
                - Confidence score (0-100)
                - List of matching past tickets
                - Short explanation of match rationale

                Your reasoning will help the system decide if this employee should be considered a strong candidate for assignment.

                
            """),
            agent=agent,
        )
    
    def skill_matcher_task(self, agent
                            ):
        return Task(
            description=dedent(f"""
                               
                You are a Skill Matcher Agent in an AI-based employee assignment system.

                Your task is to evaluate how well the selected employee's **technical skills** align with the **skills required** to complete a ticket.
                

                You will receive:
                - A list of normalized skills required for the current ticket
                - The selected employee’s skill profile (e.g., from HRMS or past projects)

                🔍 You must:
                1. Compare each required skill with the employee's known skill set
                2. Identify matching and missing skills
                3. Score the match based on skill coverage and proficiency (if available)
                4. Suggest whether this employee is a good technical fit for the ticket

                📝 Output format:
                - Skill match score (0–100)
                - List of matched and unmatched skills
                - Short justification

                Your decision will guide the assignment coordinator in final task allocation.

                
            """),
            agent=agent
        )
    
    def availability_task(self, agent
                            ):
        # additional_context = ""
        # if selected_employee:
        #     additional_context += f"\n Selected Employee for Evaluation: {selected_employee}"

        return Task(
            description=dedent(f"""
                               
                You are an Availability Agent in an AI-powered workforce management system.

                Your task is to determine whether the selected employee is currently **available** to be assigned a new ticket.

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                You will have access to:
                - Leave records (e.g., sick leave, vacation, WFH, etc.)
                - Current assignments and workload from the HRMS system
                - Employee working hours and shift schedules

                ✅ You must:
                1. Check if the employee is on leave or unavailable
                2. Review the number of ongoing assignments
                3. Assess if the employee has sufficient time and capacity to complete a new task

                📝 Output format:
                - Availability status: "Available" or "Unavailable"
                - Reason (e.g., "on sick leave", "already assigned 3 high-priority tasks")
                - Any suggested follow-up (optional)

                Your response will directly influence task allocation decisions.

            """),
            agent=agent,
        )
    
    def policy_checker_task(self, agent):
        # additional_context = ""
        # if description:
        #     additional_context += f"\nDescription/Context for the ticket: {description}"
    
        return Task(
            description=dedent(f"""
                               
                You are a Policy Checker Agent in an AI-powered workforce assignment system.

                Your role is to validate whether there are any **HR policies, rules, or department-specific restrictions** that could prevent an employee from working on a specific ticket.

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                You have access to:
                - Company-wide HR policies (via RAG or uploaded docs)
                - Department rules (e.g., Finance, Legal, IT)
                - Custom filters (e.g., "Interns can't handle client data", "Probation employees need approval")

                ✅ You must:
                1. Carefully read the task description and context
                2. Identify any red flags based on HR or department policy
                3. Flag whether assignment is allowed or restricted
                4. Mention the exact rule that was triggered if restricted

                📝 Output format:
                - status: "Allowed" or "Restricted"
                - rule_triggered: [if any] (e.g., "Interns not allowed on high-priority finance tickets")
                - explanation: (brief reason for the decision)

                Your decision will ensure all assignments stay compliant with company policies.

            """),
            agent=agent,

        )
    
    def assignment_coordinator_task(self, agent
                            ):
        return Task(
            description=dedent(f"""
                               
                You are the Assignment Coordinator Agent in an AI-powered ticket dispatch system.

                Your responsibility is to **review the final short-listed employees** and make a decision on **who should be assigned this ticket**.

                Consider all data from the previous steps:
                - Skills matching
                - Ticket history and past experience
                - Availability (leave status, workload)
                - HR & department policy restrictions

                
                Reference the market analysis when generating your ideas.
                {self.__tip_section()}

                ✅ You must:
                1. Pick the best candidate for assignment
                2. Justify your decision based on their skills, availability, and experience
                3. Ensure no policy violations exist
                4. Clearly explain **why** the selected employee is best fit for the ticket

                📝 Output format:
                - selected_employee: "Name"
                - reason: "Why this employee was chosen"
                - fallback_suggestions: ["Alt1", "Alt2"] (optional)

            """),
            agent=agent
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"
