from langchain.tools import tool
import yaml

# Load map at module level
with open(r'D:\workwise_AI\workwise\utils\skill_synonyms.yml', 'r', encoding='utf-8') as f:
    synonym_map = yaml.safe_load(f)

@tool
def normalize_skills(skills: list) -> list:
    """
    Standardizes and normalizes a list of skill names into canonical forms.
    """
    normalized = []
    for skill in skills:
        clean = skill.strip().lower()
        if clean in synonym_map:
            normalized.append(synonym_map[clean])
        else:
            normalized.append(clean.title())

    print("+++++++++++++++++++ TOOL - normalize_skills +++++++++++++++")
    print(list(set(normalized)))
    print("-----------------------------------------------------------")
    return list(set(normalized))


# ✅ Test the wrapped tool
if __name__ == "__main__":
    test_input = ["  py", "JS", "lightning web components", "css3", "Vue"]
    
    # If decorated with @tool, call using .func
    result = normalize_skills.func(test_input)
    
    print("Normalized Skills:", result)