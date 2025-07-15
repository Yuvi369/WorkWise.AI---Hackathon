from crewai import Crew
from textwrap import dedent
from bizbuddy_agents import BizBuddyAgents
from bizbuddy_tasks import BizBuddyTasks
import json
import os

from dotenv import load_dotenv
load_dotenv()

class BizBuddyCrew:

  def __init__(self, ticket_name, ticket_id, priority, description, 
                         required_skills, suggested_employees, Project, Days_to_complete, department):
    self.ticket_name = ticket_name
    self.ticket_id = ticket_id
    self.priority = priority
    self.description = description
    self.required_skills = required_skills
    self.suggested_employees = suggested_employees
    self.project = Project
    self.days_to_complete = Days_to_complete
    self.department = department

  def run(self):
    agents = BizBuddyAgents()
    tasks = BizBuddyTasks()

    ticket_analyzer_agent = agents.ticket_analyzer
    history_analyst_agent = agents.history_analyst
    skill_matcher_agent = agents.skill_matcher
    availability_agent = agents.availability
    policy_checker_agent = agents.policy_checker
    assignment_coordinator_agent = agents.assignment_coordinator

    ticket_analyzer_task  = tasks.ticket_analyzer_task(
      ticket_analyzer_agent,
      self.required_skills,
      self.description
    )

    history_analyst_task  = tasks.history_analyst_task(
      history_analyst_agent,
      self.ticket_name,
      self.ticket_id,
      self.suggested_employees
    )

    skill_matcher_task  = tasks.skill_matcher_task(
      skill_matcher_agent,
      self.suggested_employees,
      self.required_skills
    )

    availability_task  = tasks.availability_task(
      availability_agent,
      self.suggested_employees
    )

    policy_checker_task  = tasks.policy_checker_task(
      policy_checker_agent,
      self.description
    )

    assignment_coordinator_task  = tasks.assignment_coordinator_task(
      assignment_coordinator_agent,
      self.description,
      self.ticket_name,
      self.ticket_id,
      self.suggested_employees
    )

    crew = Crew(
      agents=[
        ticket_analyzer_agent, history_analyst_agent, skill_matcher_agent, availability_agent, policy_checker_agent, assignment_coordinator_agent
      ],
      tasks=[ticket_analyzer_task, history_analyst_task, skill_matcher_task, availability_task, policy_checker_task, assignment_coordinator_task],
      verbose=True
    )

    result = crew.kickoff()
    return result
  

  # Call the business logic function
        # result = process_business_info(
        #     data.get('ticket_name'),
        #     data.get('ticket_id'),
        #     data.get('priority'),
        #     data.get('description'),
        #     data.get('required_skills'),
        #     data.get('suggested_employees'),
        #     data.get('Project'),
        #     data.get('Days_to_complete'),
        #     data.get('department')
        # )
  
def assigning_requirement(ticket_name, ticket_id, priority, description, 
                         required_skills, suggested_employees, Project, Days_to_complete, department):
    """
    Process and analyzing ticket or task information provided by the user.
    """
    
    # print(f"Budget: {budget} INR")
    # print(f"Business Type: {business_type}")
    # print(f"State: {selected_state}")
    # print(f"District: {selected_district}")
    # print(f"Experience: {experience}")
    # print(f"Availability: {availability}")
    # print(f"Location Type: {location_type}")
    # print(f"Team Size: {team_size}")
    # print('-------------------------------')
    
    # Create and run the crew
    bizbuddy_crew = BizBuddyCrew(ticket_name, ticket_id, priority, description, 
                          required_skills, suggested_employees, Project, Days_to_complete, department)
    result = bizbuddy_crew.run()
    
    return {
        'ticket_name': ticket_name,
        'ticket_id': ticket_id,
        'priority': priority,
        'description': description,
        'required_skills': required_skills,
        'suggested_employees': suggested_employees,
        'Project': Project,
        'Days_to_complete': Days_to_complete,
        'department': department,
        'recommendations': result
    }

def cli_mode():
    """Run the application in command-line interface mode."""
    print('-------------------------------')
    print("*** Welcome to BizBuddy Crew. ***")
    print('Need clarification for your Business. Great!. This is the right place to get clarified. Just tell the needed info to bizbuddy. Let\'s start then....')
    print('-------------------------------')

    budget = input(
      dedent("""
        What is your planned budget (in INR) for starting the business?
      """))
    business_type = input(
      dedent("""
          What type of business are you planning to start?
            Choose one of the following examples:
            1. Retail
            2. Manufacturing
            3. Service
            4. E-commerce
      """))
    selected_state = input(
      dedent("""
          In which state do you plan to start your business?
            Example options:
            1. Tamil Nadu
            2. Andhra Pradesh
            3. Karnataka
            4. Kerala 
      """))
    selected_district = input(
      dedent("""
          In which district of the selected state will the business be located?
            Example options:
            1. Madurai
            2. Chennai
            3. Theni
      """))
    experience = input(
      dedent("""
          Do you have any prior experience or skills relevant to the business? 
          (e.g., cooking, digital marketing, repair work, sales, etc.)
      """))
    availability = input(
      dedent("""
          How much time can you dedicate to running this business? 
          (e.g., Full-time, Part-time, Weekends only)
      """))
    location_type = input(
      dedent("""
          Where do you plan to operate your business from?
          1. Home
          2. Rented Shop
          3. Online only
          4. Shared Workspace
      """))
    team_size = input(
      dedent("""
          Are you planning to start this business alone or with a partner/team?
      """))
    
    # Process the information
    result = process_business_info(
        budget, business_type, selected_state, selected_district,
        experience, availability, location_type, team_size
    )
    
    # Save the result to a file
    with open('business_info.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n\n########################")
    print("## Here is your Business Recommendation")
    print("########################\n")
    print(result['recommendations'])
    print("\nThank you for using BizBuddy. Your business data has been saved to business_info.json.")


if __name__ == "__main__":
    # Check if we're running from the web app with arguments
    if os.environ.get('WEB_MODE') == 'True':
        # Web mode - don't execute CLI code
        pass
    else:
        # Default to CLI mode
        cli_mode()

# if __name__ == "__main__":
#   print('-------------------------------')
#   print("*** Welcome to BizBuddy Crew. ***")
#   print('Need clarification for your Business. Great!. This is the right place to get clarified. Just tell the needed info to bizbuddy. Let''s start then....')
#   print('-------------------------------')

#   budget = input(
#     dedent("""
#       What is your planned budget (in INR) for starting the business?
#     """))
#   business_type = input(
#     dedent("""
#         What type of business are you planning to start?
#           Choose one of the following examples:
#           1. Retail
#           2. Manufacturing
#           3. Service
#           4. E-commerce
#     """))
#   selected_state = input(
#     dedent("""
#         In which state do you plan to start your business?
#           Example options:
#           1. Tamil Nadu
#           2. Andhra Pradesh
#           3. Karnataka
#           4. Kerala 
#     """))
#   selected_district = input(
#     dedent("""
#         In which district of the selected state will the business be located?
#           Example options:
#           1. Madurai
#           2. Chennai
#           3. Theni
#     """))
#   experience = input(
#     dedent("""
#         Do you have any prior experience or skills relevant to the business? 
#         (e.g., cooking, digital marketing, repair work, sales, etc.)
#     """))
#   availability = input(
#     dedent("""
#         How much time can you dedicate to running this business? 
#         (e.g., Full-time, Part-time, Weekends only)
#     """))
#   location_type = input(
#     dedent("""
#         Where do you plan to operate your business from?
#         1. Home
#         2. Rented Shop
#         3. Online only
#         4. Shared Workspace
#     """))
#   team_size = input(
#     dedent("""
#         Are you planning to start this business alone or with a partner/team?
#     """))

  
#   trip_crew = BizBuddyCrew(budget, business_type, selected_state, selected_district, experience, availability, location_type, team_size)
#   result = trip_crew.run()
#   print("\n\n########################")
#   print("## Here is you Business Plan")
#   print("########################\n")
#   print(result)
