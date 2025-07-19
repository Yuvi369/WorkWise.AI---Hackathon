from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os

load_dotenv()


def get_llm(model_name):
    if model_name == "gemini-2.0-flash":
        google_api_key = os.getenv("GOOGLE_API_KEY")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=google_api_key
        )

    elif model_name in ["gpt-4o", "gpt-3.5-turbo"]:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(
            model=model_name,
            api_key=openai_api_key
        )
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    return llm