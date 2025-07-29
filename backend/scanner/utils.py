import re
from typing import List

def load_code_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def sanitize_code(code: str) -> str:
    code = re.sub(r"/\*[\s\S]*?\*/", "", code)
    code = re.sub(r"<!--[\s\S]*?-->", "", code)
    code = re.sub(r"(?<!:)//.*", "", code)
    code = re.sub(r"#.*", "", code)
    code = re.sub(r"\n\s*\n", "\n", code)
    return code.strip()

def extract_keywords(text: str) -> List[str]:
    """
    Naively extracts OWASP-related keywords (vulnerability types) from LLM output.
    You can later replace this with a more robust parser or JSON-based response.
    """
    owasp_keywords = [
        "SQL Injection", "XSS", "Cross-Site Scripting", "Command Injection", "Insecure Deserialization",
        "Sensitive Data Exposure", "Security Misconfiguration", "Broken Access Control",
        "Broken Authentication", "Cross-Site Request Forgery", "CSRF", "Path Traversal", "IDOR"
    ]

    found = []
    for keyword in owasp_keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
            found.append(keyword)

    return list(set(found))  # remove duplicates
