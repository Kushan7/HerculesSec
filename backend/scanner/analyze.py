import os
from typing import Dict, Any, List

from backend.scanner.utils import load_code_file, sanitize_code, extract_keywords
from backend.llm.openai_integration import ask_llm_with_prompt
from backend.db.exploitdb_lookup import search_exploitdb

PROMPT_FILE = "backend/llm/prompts/owasp_top10.txt"

def analyze_code_with_llm(file_path: str) -> Dict[str, Any]:
    try:
        raw_code = load_code_file(file_path)
        clean_code = sanitize_code(raw_code)

        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            prompt_instructions = f.read()

        full_prompt = f"""{prompt_instructions}

Code:

{clean_code}
"""

        response = ask_llm_with_prompt(full_prompt)

        # Extract keywords like "XSS", "SQL Injection"
        enrichments = []
        for vuln in extract_keywords(response):
            matched_exploits = search_exploitdb(vuln)
            if matched_exploits:
                enrichments.append({vuln: matched_exploits})

        return {
            "file": os.path.basename(file_path),
            "vulnerabilities": response,
            "exploitdb_links": enrichments
        }

    except Exception as e:
        return {
            "file": os.path.basename(file_path),
            "error": str(e)
        }
