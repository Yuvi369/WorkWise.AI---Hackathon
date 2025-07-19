import os
import json
import time
from base_agent import BaseAgent, Message, MessageType, Tool
from tools_camel.enrich_skill_tool import enrich_skills_with_llm
from tools_camel.normalize_skills_tools import normalize_skills

# Create tool wrappers for the agent
class SkillNormalizationTool(Tool):
    def __init__(self):
        super().__init__("normalize_skills", "Normalizes and standardizes skill names")
    
    def execute(self, params):
        skills = params.get("skills", [])
        return normalize_skills(skills)

class SkillEnrichmentTool(Tool):
    def __init__(self):
        super().__init__("enrich_skills_with_llm", "Enriches skills using LLM analysis of description")
    
    def execute(self, params):
        description = params.get("description", "")
        existing_skills = params.get("existing_skills", "")
        return enrich_skills_with_llm(description, existing_skills)

class TicketAnalyzerAgents(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ticket_analyzer",
            role="Ticket Understanding & Skill Extraction",
            specialization="""You are a seasoned product analyst who has worked across hundreds of agile teams.
            You are great at understanding vague or incomplete ticket descriptions and extracting the relevant skills required."""
        )
        
        print("*****^^^^^^####### Ticket Analyzer agent execution started *****^^^^^^#######")
        # Register tools with the agent
        self.add_tool(SkillNormalizationTool())
        self.add_tool(SkillEnrichmentTool())

    def analyze_employee_for_ticket(self, input_skills: list, description: str, existing_skills: str) -> dict:
        """Direct analysis method for ticket skill extraction"""
        try:
            # Normalize skills using the tool
            normalized = normalize_skills(input_skills)
            
            # Enrich skills using the tool
            enriched = enrich_skills_with_llm(description, existing_skills)
            
            return {
                "normalized_skills": normalized,
                "enriched_skills": enriched
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "normalized_skills": None,
                "enriched_skills": None
            }

    def analyze_with_agent_system(self, input_skills: list, description: str, existing_skills: str):
        """Uses the agent's messaging system with tool prompting"""
        
        # Create a task message with tool usage instructions
        task_content = f"""
        Please analyze this ticket for skill extraction and normalization:
        
        Input Skills: {input_skills}
        Ticket Description: {description}
        Existing Skills: {existing_skills}

        Please follow these steps:
        1. Use the normalize_skills tool with the "Input Skills" to standardize the skill names
        2. Use the enrich_skills_with_llm tool with the "Ticket Description" and "Existing Skills" to identify additional relevant skills
        
        Provide a comprehensive analysis of the required skills for this ticket.
        """
        
        message = Message(
            sender="system",
            receiver=self.name,
            message_type=MessageType.TASK_ASSIGNMENT,
            content=task_content,
            timestamp=time.time()
        )
        
        # Process the message through agent system
        response = self.process_message(message)
        print("*****^^^^^^####### Ticket Analyzer agent execution Completed *****^^^^^^#######")
        return response

if __name__ == "__main__":
    print("🚀 Starting TicketAnalyzerAgents Test")
    print("=" * 60)
    
    try:
        agent = TicketAnalyzerAgents()
        print("✅ TicketAnalyzerAgents created successfully")
        print(f"🔧 Available tools: {list(agent.tools.keys())}")
        
        # Test data
        test_input = ["  py", "JS", "lightning web components", "css3", "Vue"]
        description = "Fix button layout issues and apply responsive design in LWC component."
        existing_skills = "LWC, CSS"
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 1: Direct Analysis (Tool Execution)")
        print("=" * 60)
        
        result1 = agent.analyze_employee_for_ticket(test_input, description, existing_skills)
        print(":dart: Ticket Analysis Result:")
        print(json.dumps(result1, indent=2))
        
        print("\n" + "=" * 60)
        print("🧪 METHOD 2: Agent System Analysis (With Prompting)")
        print("=" * 60)
        
        result2 = agent.analyze_with_agent_system(test_input, description, existing_skills)
        
        if result2:
            print("🤖 Agent Response:")
            print(f"📤 From: {result2.sender}")
            print(f"📥 To: {result2.receiver}")
            print(f"📋 Type: {result2.message_type}")
            print(f"💬 Content: {result2.content}")
        else:
            print("❌ No response from agent")
        
        print("\n" + "=" * 60)
        print("🏁 TEST COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 MAIN ERROR: {e}")
        import traceback
        traceback.print_exc()