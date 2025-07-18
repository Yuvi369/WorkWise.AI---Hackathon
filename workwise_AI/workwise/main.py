import sys
import os

# Dynamically add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from crewai import Crew
from textwrap import dedent
from ticket_agents import TicketAnalyzerAgents
from ticket_tasks import TicketAnalyzerTasks
import json
import os

from dotenv import load_dotenv
load_dotenv()

class TicketAnalyzerCrew:

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
    agents = TicketAnalyzerAgents()
    tasks = TicketAnalyzerTasks()

    ticket_analyzer_agent = agents.ticket_analyzer(self.required_skills, self.description)
    history_analyst_agent = agents.history_analyst(self.suggested_employees, self.description, self.required_skills, self.ticket_name)
    skill_matcher_agent = agents.skill_matcher(self.suggested_employees)
    availability_agent = agents.availability
    policy_checker_agent = agents.policy_checker(self.ticket_name, self.ticket_id, self.description, self.suggested_employees, r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_leave_1.xlsx", "name")
    assignment_coordinator_agent = agents.assignment_coordinator

    ticket_analyzer_task  = tasks.ticket_analyzer_task(
      ticket_analyzer_agent
      # self.required_skills,
      # self.description
    )

    history_analyst_task  = tasks.history_analyst_task(
      history_analyst_agent
      # self.ticket_name,
      # self.ticket_id,
      # self.suggested_employees
    )

    skill_matcher_task  = tasks.skill_matcher_task(
      skill_matcher_agent
      # self.suggested_employees,
      # self.required_skills
    )

    availability_task  = tasks.availability_task(
      availability_agent
      #self.suggested_employees
    )

    policy_checker_task  = tasks.policy_checker_task(
      policy_checker_agent
      #self.description
    )

    assignment_coordinator_task  = tasks.assignment_coordinator_task(
      assignment_coordinator_agent
      # self.description,
      # self.ticket_name,
      # self.ticket_id,
      # self.suggested_employees
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


def unpack_json(request_json):
   ticket_name = request_json.get("ticket_name", "Unknown")
   ticket_id = request_json.get("ticket_id", "Unknown")
   priority = request_json.get("priority", "Unknown")
   description = request_json.get("description", "Unknown")
   required_skills = request_json.get("required_skills", "Unknown")
   suggested_employees = request_json.get("suggested_employees", "Unknown")
   project = request_json.get("project", "Unknown")
   days_to_complete = request_json.get("days_to_complete", "Unknown")
   department = request_json.get("department", "Unknown")

   ticket_obj = TicketAnalyzerCrew(ticket_name, ticket_id, priority,
                                    description, required_skills, suggested_employees,
                                    project, days_to_complete, department)
   
   result = ticket_obj.run()

   print("^%^%&**" * 60)
   print("-------------- FInal result Task ------------------")
   print(result)

  #  return {
  #       'ticket_name': ticket_name,
  #       'ticket_id': ticket_id,
  #       'priority': priority,
  #       'description': description,
  #       'required_skills': required_skills,
  #       'suggested_employees': suggested_employees,
  #       'Project': Project,
  #       'Days_to_complete': Days_to_complete,
  #       'department': department,
  #       'recommendations': result
  #   }


if __name__ == "__main__":
    
    config = {
       "ticket_name" : "UI Production Issue",
       "ticket_id" : "FS-888",
       "priority" : "High",
       "description" : "Important ticket.fix the ui bug fix",
       "required_skills" : ['React', 'CSS', 'Production-deployment-experience', 'mongodb', 'bug-handling'],
       "suggested_employees" : ["Mark Jenkins", "Kenneth Green", "Amanda Lewis"],
       "project" : "Full Stack",
       "days_to_complete" : "4"
      #  "department" : ""
    }

    unpack_json(config)