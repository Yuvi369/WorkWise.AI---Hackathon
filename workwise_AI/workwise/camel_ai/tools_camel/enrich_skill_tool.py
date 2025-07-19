# enrich_skills_with_llm.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.tools import tool
import ast
import yaml
import re

# Load env variables
load_dotenv()

# Load the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def load_prompt():
    with open(r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\utils\enrich_skills_prompt.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["enrich_skills_prompt"]

def enrich_skills_with_llm(description: str, existing_skills: str = "") -> list:
    """
    Uses Gemini to infer relevant skills from a ticket description and merges them with existing ones.
    
    Args:
        description: The ticket description to analyze
        existing_skills: Comma-separated string of existing skills (optional)
    
    Returns:
        List of enriched skills combined with existing skills
    """
    try:
        # Convert existing_skills string to list if provided
        existing_skills_list = []
        if existing_skills:
            if isinstance(existing_skills, str):
                existing_skills_list = [skill.strip() for skill in existing_skills.split(",") if skill.strip()]
            elif isinstance(existing_skills, list):
                existing_skills_list = existing_skills
        
        prompt_template = load_prompt()
        formatted_prompt = prompt_template.format(
            description=description,
            existing_skills=", ".join(existing_skills_list) if existing_skills_list else "None"
        )

        response = model.generate_content(formatted_prompt)
        raw = response.text.strip()

        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            enriched = ast.literal_eval(match.group(0))
        else:
            raise ValueError(f"No valid list found in response: {raw}")
        
        print("+++++++++++++++++++ TOOL - Enrich_skills +++++++++++++++")
        print(sorted(list(set(enriched + existing_skills_list))))
        print("-----------------------------------------------------------")

        return sorted(list(set(enriched + existing_skills_list)))

    except Exception as e:
        print("❌ Gemini Enrichment Failed:", e)
        return existing_skills_list if existing_skills_list else []

# Test function
if __name__ == "__main__":
    result = enrich_skills_with_llm.func(
        description="Fix button layout issues and apply responsive design in LWC component.",
        existing_skills="LWC, CSS"
    )
    print("🧠 Enriched Skills:", result)