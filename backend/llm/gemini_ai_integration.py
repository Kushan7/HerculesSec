import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Gemini with your API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model_name = "models/gemini-1.5-pro"  # Use proper model path
model = genai.GenerativeModel(model_name)

def analyze_code_with_gemini(file_content: str) -> str:
    """
    Analyzes the given code using Google's Gemini model for OWASP Top 10 vulnerabilities.
    Returns the response as text or an error message.
    """
    prompt = f"""
You are a security expert. Analyze the following code for OWASP Top 10 vulnerabilities.
Explain what vulnerabilities exist, their severity, and how to fix them.

Code:

Respond in JSON format like:
{{
  "vulnerabilities": [
    {{
      "type": "XSS",
      "severity": "High",
      "line": 23,
      "explanation": "..."
    }},
    ...
  ]
}}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# Optional: Quick test if running directly
if __name__ == "__main__":
    sample_code = "<script>alert('hello')</script>"
    print(analyze_code_with_gemini(sample_code))
