import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_llm_with_prompt(prompt: str, temperature: float = 0.2) -> str:
    """
    Sends the prompt to GPT-4 if available, otherwise falls back to GPT-3.5-Turbo.
    """
    system_message = {
        "role": "system",
        "content": "You're a bug bounty hunter and secure code analysis expert. Analyze vulnerabilities based on OWASP Top 10."
    }
    user_message = {"role": "user", "content": prompt}

    for model in ["gpt-4", "gpt-3.5-turbo"]:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[system_message, user_message],
                temperature=temperature,
                max_tokens=1500
            )
            return f"[{model.upper()}]\n" + response.choices[0].message.content.strip()
        except Exception as e:
            if "model_not_found" in str(e):
                continue  # Try next model
            return f"Error from LLM: {str(e)}"

    return "Error: No supported OpenAI model available or accessible."
print("API KEY:", os.getenv("OPENAI_API_KEY"))
