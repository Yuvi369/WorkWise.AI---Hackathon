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
    with open(r"workwise\utils\enrich_skills_prompt.yml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["enrich_skills_prompt"]


@tool
def enrich_skills_with_llm(description: str, existing_skills: list = []) -> list:
    """
    Uses Gemini to infer relevant skills from a ticket description and merges them with existing ones.
    """
    try:
        prompt_template = load_prompt()
        formatted_prompt = prompt_template.format(
            description=description,
            existing_skills=", ".join(existing_skills) if existing_skills else "None"
        )

        response = model.generate_content(formatted_prompt)
        raw = response.text.strip()

        print(f'RESPONSE FROM LLM == enrich_skill_tool : {raw}')

        # # Safe parsing
        # enriched = ast.literal_eval(raw)

        # return sorted(list(set(enriched + existing_skills)))

        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            enriched = ast.literal_eval(match.group(0))
        else:
            raise ValueError(f"No valid list found in response: {raw}")

        return sorted(list(set(enriched + existing_skills)))

    except Exception as e:
        print("❌ Gemini Enrichment Failed:", e)
        return existing_skills


if __name__ == "__main__":
    result = enrich_skills_with_llm.func(
        description="Fix button layout issues and apply responsive design in LWC component.",
        existing_skills=["LWC"]
    )
    print("🧠 Enriched Skills:", result)
