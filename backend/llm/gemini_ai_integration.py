import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

# Load .env variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Correct model name for Gemini
model = genai.GenerativeModel("gemini-1.5-pro")

def analyze_code_with_gemini(file_content: str, max_retries=4) -> str:
    """
    Analyze code using Gemini for OWASP Top 10 vulnerabilities.
    Returns a JSON-style string with vulnerabilities or an error.
    """

    prompt = f"""
You are a security expert. Analyze the following code for OWASP Top 10 vulnerabilities.
Explain what vulnerabilities exist, their severity, and how to fix them.

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

Code:
    """

    retries = 0
    delay = 8  # initial wait

    while retries < max_retries:
        try:
            response = model.generate_content(prompt)
            return response.text

        except ResourceExhausted as e:
            print(f"[Gemini] Quota exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)
            retries += 1
            delay *= 2  # exponential backoff

        except Exception as e:
            print(f"[Gemini] Unexpected error: {e}")
            return f"Gemini Error: {str(e)}"

    return "Gemini Error: Reached max retries due to quota exhaustion."

# For direct testing
if __name__ == "__main__":
    test_code = "<script>alert('hello')</script>"
    result = analyze_code_with_gemini(test_code)
    print(result)
