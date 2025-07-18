import google.generativeai as genai
from instructions import return_instructions
import os
import json
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Load the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# System instruction for Gemini
system_instruction = return_instructions()

# Create chat model using Gemini 1.5 Flash
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# Start a chat
chat = model.start_chat()

# File path to save JSON output
OUTPUT_JSON_PATH = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\chat_gemini\extracted_json.json"

def chat_main(user_prompt=None):
    # Example input if not provided
    if not user_prompt:
        user_prompt = """
        This is a high priority ticket. "
        Show the assignee report for this ticket Ticket Name: API Endpoint Not Responding.
        """

    # Send message to Gemini
    response = chat.send_message(user_prompt)
    response_text = response.text.strip()

    print("Structured Output:")
    print(response_text)

    # Try parsing and saving response
    try:
        # Fix Gemini response if it's wrapped in triple backticks or markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text.lstrip("```json").rstrip("```").strip()

        parsed_json = json.loads(response_text)

        # Optional: Check for required fields manually
        required_fields = ["ticket_name", "ticket_number", "description"]
        missing_fields = [field for field in required_fields if not parsed_json.get(field)]

        if missing_fields:
            print(f"\n⚠️ Missing required fields: {', '.join(missing_fields)}")
            print("❌ JSON not saved. Please provide the missing fields and try again.")
            return

        # Save to JSON file
        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as json_file:
            json.dump(parsed_json, json_file, indent=4, ensure_ascii=False)

        print(f"\n✅ JSON saved successfully at:\n{OUTPUT_JSON_PATH}")
    except Exception as e:
        print("\n❌ Failed to parse or save JSON:")
        print(e)

if __name__ == "__main__":
    chat_main()
