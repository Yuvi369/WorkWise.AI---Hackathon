from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogAssignmentInput(BaseModel):
    """Input schema for log_assignment tool."""
    ticket_name: str = Field(..., description="Name of the ticket being assigned")
    ticket_description: str = Field(..., description="Description of the ticket")
    selected_employee: str = Field(..., description="Name of the employee selected for assignment")
    assignment_reason: str = Field(..., description="Detailed reason why this employee was selected")
    skill_match_score: float = Field(..., description="Skill matching score (0-1)")
    availability_score: float = Field(..., description="Availability score (0-1)")
    experience_score: float = Field(..., description="Experience/history score (0-1)")
    policy_compliance: bool = Field(..., description="Whether assignment complies with policies")
    final_score: float = Field(..., description="Final weighted score for the selected employee")
    assignment_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="When assignment was made")
    assigned_by: str = Field(default="Assignment Coordinator Agent", description="Who made the assignment")

@tool(args_schema=LogAssignmentInput)
def log_assignment(**kwargs) -> str:
    """Logs the final employee assignment decision with all relevant details and reasoning."""
    try:
        # Extract input parameters
        ticket_name = kwargs.get('ticket_name')
        ticket_description = kwargs.get('ticket_description')
        selected_employee = kwargs.get('selected_employee')
        assignment_reason = kwargs.get('assignment_reason')
        skill_match_score = kwargs.get('skill_match_score')
        availability_score = kwargs.get('availability_score')
        experience_score = kwargs.get('experience_score')
        policy_compliance = kwargs.get('policy_compliance')
        final_score = kwargs.get('final_score')
        assignment_timestamp = kwargs.get('assignment_timestamp', datetime.now().isoformat())
        assigned_by = kwargs.get('assigned_by', "Assignment Coordinator Agent")

        # Create assignment record
        assignment_record = {
            "ticket_id": f"TICKET_{ticket_name.replace(' ', '_').upper()}",
            "ticket_name": ticket_name,
            "ticket_description": ticket_description,
            "assignment_details": {
                "selected_employee": selected_employee,
                "assignment_reason": assignment_reason,
                "assigned_by": assigned_by,
                "assignment_timestamp": assignment_timestamp
            },
            "scoring_breakdown": {
                "skill_match_score": skill_match_score,
                "availability_score": availability_score,
                "experience_score": experience_score,
                "final_score": final_score
            },
            "policy_compliance": policy_compliance,
            "status": "ASSIGNED"
        }

        # Log the assignment (can be saved to DB)
        logger.info(f"ASSIGNMENT LOGGED: {json.dumps(assignment_record, indent=2)}")

        # Simulated workload update
        logger.info(f"Updated workload for {selected_employee}: Added ticket '{ticket_name}'")

        # Generate confirmation message
        confirmation_message = f"""
✅ ASSIGNMENT COMPLETED SUCCESSFULLY

📋 Ticket: {ticket_name}
👤 Assigned To: {selected_employee}
📊 Final Score: {final_score:.3f}
⏰ Assigned At: {assignment_timestamp}

🎯 Assignment Reasoning:
{assignment_reason}

📈 Score Breakdown:
• Skill Match: {skill_match_score:.3f}
• Availability: {availability_score:.3f}
• Experience: {experience_score:.3f}
• Policy Compliant: {'✅ Yes' if policy_compliance else '❌ No'}

The assignment has been logged and the employee has been notified.
        """

        return confirmation_message.strip()

    except Exception as e:
        error_message = f"❌ Failed to log assignment: {str(e)}"
        logger.error(error_message)
        return error_message

if __name__ == "__main__":
    from pprint import pprint

    input_data = {
        "ticket_name": "Fix UI Bug",
        "ticket_description": "Alignment issue on the homepage in Firefox.",
        "selected_employee": "John Doe",
        "assignment_reason": "Most experience with frontend layout bugs.",
        "skill_match_score": 0.92,
        "availability_score": 0.87,
        "experience_score": 0.95,
        "policy_compliance": True,
        "final_score": 0.91
    }

    result = log_assignment.func(**input_data)
    pprint(result)
