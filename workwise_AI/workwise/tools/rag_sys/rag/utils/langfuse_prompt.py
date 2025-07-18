import os
from langfuse import Langfuse

_langfuse_client = None

def get_langfuse_client():
    """Returns a singleton Langfuse client instance."""
    global _langfuse_client
    
    if _langfuse_client is None:
        _langfuse_client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )
    
    return _langfuse_client

def get_system_prompt(prompt_name: str) -> str:
    try:
        langfuse = get_langfuse_client()      
        prompt = langfuse.get_prompt(prompt_name)      
        print(f"Fetched prompt '{prompt_name}'")
        return prompt.prompt
    except Exception as e:
        print(f"Error fetching prompt from Langfuse: {e}")
        default_prompt = (
            "You are a helpful assistant tasked with determining whether an employee can be assigned a ticket based on their profile and the ticket description. "
            "Using the provided context, evaluate the employee's eligibility. "
            "Return only a JSON object with two fields: "
            "'decision' (a string stating whether the employee can be assigned the ticket and why), "
            "and 'flag' (1 if the employee can be assigned, 0 if they cannot). "
            "Example: {{\"decision\": \"Employee cannot be assigned due to insufficient experience\", \"flag\": 0}}. "
            "Context: {context}"
        )
        print(f"Using default system prompt for '{prompt_name}'")
        return default_prompt