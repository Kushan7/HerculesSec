import os
from typing import Dict, Any, List

from backend.scanner.utils import load_code_file, sanitize_code, extract_keywords
from backend.llm.gemini_ai_integration import analyze_code_with_gemini
from backend.db.exploitdb_lookup import search_exploitdb
import json

def analyze_file_for_vulnerabilities(file_path: str) -> Dict[str, Any]:
    try:
        raw_code = load_code_file(file_path)
        clean_code = sanitize_code(raw_code)

        # Call Gemini model to analyze code
        llm_response = analyze_code_with_gemini(clean_code)

        try:
            parsed_response = json.loads(llm_response)
            vulnerabilities = parsed_response.get("vulnerabilities", [])
        except json.JSONDecodeError:
            # If LLM didn't return valid JSON, return the raw text
            vulnerabilities = llm_response

        # Enrich results with ExploitDB links
        enrichments = []
        if isinstance(vulnerabilities, list):
            for vuln in vulnerabilities:
                vuln_type = vuln.get("type")
                if vuln_type:
                    matched_exploits = search_exploitdb(vuln_type)
                    if matched_exploits:
                        enrichments.append({vuln_type: matched_exploits})

        return {
            "file": os.path.basename(file_path),
            "vulnerabilities": vulnerabilities,
            "exploitdb_links": enrichments
        }

    except Exception as e:
        return {
            "file": os.path.basename(file_path),
            "error": str(e)
        }
