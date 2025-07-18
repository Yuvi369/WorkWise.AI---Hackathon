import os
import json
import re
from typing import Dict, List, Any
from base_agent import BaseAgent, Tool, TicketData, MessageType
import google.generativeai as genai

class NormalizeSkillsTool(Tool):
    def __init__(self):
        super().__init__("normalize_skills", "Normalize and standardize skill names")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        skills = params.get("skills", [])
        
        # Skill normalization mapping
        skill_mapping = {
            "js": "javascript",
            "py": "python",
            "react.js": "react",
            "node.js": "nodejs",
            "html5": "html",
            "css3": "css",
            "sql server": "sql",
            "mysql": "sql",
            "postgresql": "sql",
            "mongodb": "nosql",
            "aws": "cloud",
            "azure": "cloud",
            "gcp": "cloud",
            "docker": "containerization",
            "kubernetes": "orchestration",
            "jenkins": "ci/cd",
            "git": "version_control",
            "github": "version_control",
            "gitlab": "version_control"
        }
        
        normalized_skills = []
        for skill in skills:
            skill_lower = skill.lower().strip()
            normalized_skill = skill_mapping.get(skill_lower, skill_lower)
            if normalized_skill not in normalized_skills:
                normalized_skills.append(normalized_skill)
        
        return {
            "status": "success",
            "original_skills": skills,
            "normalized_skills": normalized_skills,
            "mappings_applied": len([s for s in skills if s.lower() in skill_mapping])
        }

class EnrichSkillsWithLLMTool(Tool):
    def __init__(self):
        super().__init__("enrich_skills_with_llm", "Enrich skills using LLM analysis")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        ticket_description = params.get("ticket_description", "")
        existing_skills = params.get("existing_skills", [])
        
        prompt = f"""
        Analyze this ticket description and identify required technical skills:
        
        Ticket Description: {ticket_description}
        
        Existing identified skills: {existing_skills}
        
        Please identify:
        1. Additional technical skills needed
        2. Skill level required (1-5, where 5 is expert)
        3. Priority of each skill for this ticket
        
        Return response in JSON format:
        {{
            "additional_skills": ["skill1", "skill2"],
            "skill_levels": {{"skill": level}},
            "skill_priorities": {{"skill": priority}}
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON from response
            response_text = response.text
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                enriched_data = json.loads(json_match.group())
            else:
                enriched_data = {"additional_skills": [], "skill_levels": {}, "skill_priorities": {}}
            
            return {
                "status": "success",
                "enriched_skills": enriched_data,
                "total_skills": len(existing_skills) + len(enriched_data.get("additional_skills", [])),
                "llm_analysis": response_text
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "enriched_skills": {"additional_skills": [], "skill_levels": {}, "skill_priorities": {}}
            }

class TicketAnalyzer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ticket_analyzer",
            role="Ticket Analysis Specialist",
            specialization="analyzing tickets and extracting required skills"
        )
        
        # Add tools
        self.add_tool(NormalizeSkillsTool())
        self.add_tool(EnrichSkillsWithLLMTool())
    
    def analyze_ticket(self, ticket_data: TicketData) -> Dict[str, Any]:
        """Main method to analyze a ticket and extract skills"""
        
        # Step 1: Normalize existing skills
        normalize_result = self.tools["normalize_skills"].execute({
            "skills": ticket_data.required_skills
        })
        
        # Step 2: Enrich skills with LLM
        enrich_result = self.tools["enrich_skills_with_llm"].execute({
            "ticket_description": ticket_data.description,
            "existing_skills": normalize_result["normalized_skills"]
        })
        
        # Combine results
        all_skills = normalize_result["normalized_skills"] + enrich_result["enriched_skills"]["additional_skills"]
        
        analysis_result = {
            "ticket_id": ticket_data.ticket_id,
            "title": ticket_data.title,
            "priority": ticket_data.priority,
            "category": ticket_data.category,
            "required_skills": list(set(all_skills)),  # Remove duplicates
            "skill_levels": enrich_result["enriched_skills"].get("skill_levels", {}),
            "skill_priorities": enrich_result["enriched_skills"].get("skill_priorities", {}),
            "estimated_hours": ticket_data.estimated_hours,
            "deadline": ticket_data.deadline,
            "complexity_score": self._calculate_complexity(ticket_data, all_skills),
            "analysis_metadata": {
                "normalized_skills": normalize_result["normalized_skills"],
                "enriched_skills": enrich_result["enriched_skills"]["additional_skills"],
                "normalization_mappings": normalize_result["mappings_applied"]
            }
        }
        
        return analysis_result
    
    def _calculate_complexity(self, ticket_data: TicketData, skills: List[str]) -> int:
        """Calculate ticket complexity score (1-10)"""
        complexity = 1
        
        # Priority factor
        priority_scores = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
        complexity += priority_scores.get(ticket_data.priority.lower(), 1)
        
        # Skills count factor
        complexity += min(len(skills), 3)  # Max 3 points for skills
        
        # Estimated hours factor
        if ticket_data.estimated_hours > 40:
            complexity += 3
        elif ticket_data.estimated_hours > 20:
            complexity += 2
        elif ticket_data.estimated_hours > 10:
            complexity += 1
        
        return min(complexity, 10)  # Cap at 10

# Example usage
if __name__ == "__main__":
    # Test the Ticket Analyzer
    analyzer = TicketAnalyzer()
    
    # Sample ticket data
    ticket = TicketData(
        ticket_id="TICK-001",
        title="Build React Dashboard with API Integration",
        description="Create a responsive dashboard using React.js with REST API integration. Need to display real-time data charts and implement user authentication. Backend should use Node.js with MongoDB.",
        priority="high",
        required_skills=["react.js", "nodejs", "mongodb"],
        estimated_hours=35,
        deadline="2024-12-31",
        category="frontend"
    )
    
    result = analyzer.analyze_ticket(ticket)
    print("🎯 Ticket Analysis Result:")
    print(json.dumps(result, indent=2))