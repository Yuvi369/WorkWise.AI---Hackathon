from crewai import Agent
from langchain.tools import tool, BaseTool
from pydantic import BaseModel, Field

from typing import List, Optional

from tools.enrich_skill_tool import enrich_skills_with_llm
from tools.normalize_skills_tools import normalize_skills

class NormalizeAndEnrichSkillsInput(BaseModel):
    description: str = Field(..., description="The ticket description to analyze")
    existing_skills: Optional[List[str]] = Field(default=[], description="List of existing skills provided")

class NormalizeAndEnrichSkillsTool(BaseTool):
    name: str = "normalize_and_enrich_skills"
    description: str = """
    Analyzes a ticket description and processes skills in two steps:
    1. Enriches existing skills with relevant skills inferred from the ticket description
    2. Normalizes all skills to canonical forms using synonym mapping
    
    Input: ticket description (required) and existing skills list (optional)
    Output: A clean, normalized list of all relevant skills
    """
    args_schema = NormalizeAndEnrichSkillsInput

    def _run(self, description: str, existing_skills: List[str] = None) -> List[str]:
        if existing_skills is None:
            existing_skills = []
        
        print("🔧 Starting skill processing pipeline...")
        
        # Step 1: Enrich skills using LLM
        enriched_skills = enrich_skills_with_llm.func(description, existing_skills)
        
        # Step 2: Normalize the enriched skills
        normalized_skills = normalize_skills.func(enriched_skills)
        
        print("✅ Skill processing complete!")
        return normalized_skills