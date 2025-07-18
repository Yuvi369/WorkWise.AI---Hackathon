# Add this at the beginning of your script to debug
import os
import google.generativeai as genai

# Check if API key is loaded
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key is not None}")
print(f"API Key length: {len(api_key) if api_key else 0}")

# Try a simple test
try:
    genai.configure(api_key=api_key)
    
    # List available models to test connection
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"Available model: {model.name}")
            break
    
    # Test with a simple prompt
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, this is a test.")
    print("Test successful!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")