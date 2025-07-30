
# 🔒 Hercules Secure - LLM-based Vibe Code Vulnerability Scanner

Hercules Secure is an AI-powered backend microservice designed to scan uploaded source code files for OWASP Top 10 vulnerabilities using **Google Gemini 1.5 Pro API**. The tool performs a deep vulnerability analysis using advanced LLMs and responds in structured JSON format with issues, severity, and remediation.

---

## 🚀 Features

- Upload and scan any code file (`.py`, `.js`, `.php`, etc.)
- Uses Gemini LLM to detect:
  - XSS
  - SQLi
  - CSRF
  - Insecure Deserialization
  - Broken Auth, etc.
- Outputs vulnerability reports in JSON format
- Easy to plug into your CI/CD pipeline or dashboard

---

## 📦 Folder Structure

```
hercules-secure/
│
├── backend/
│   ├── scanner/
│   │   └── analyze.py      # Gemini-based code analyzer
│   └── routes/
│       └── scan.py         # FastAPI upload + processing route
│
├── main.py                 # FastAPI app launcher
├── .env                    # Your Gemini API key
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-org/hercules-secure
cd hercules-secure
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Create a `.env` file in the root folder:

```ini
GEMINI_API_KEY=your_google_api_key_here
```

> ⚠️ You need access to the [Google AI Studio](https://makersuite.google.com/app) and have an API key from Google’s Generative AI platform.

---

## 🧪 Run the API Server

```bash
uvicorn main:app --reload
```

Server will run at:  
👉 `http://127.0.0.1:8000/scan`

---

## 📤 API Usage

### Endpoint: `POST /scan`

#### Upload a file:
Use Postman or curl:

```bash
curl -X POST "http://localhost:8000/scan" \
     -H  "accept: application/json" \
     -H  "Content-Type: multipart/form-data" \
     -F "file=@sample_vuln_code.js"
```

#### ✅ Successful Response

```json
{
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "severity": "Critical",
      "line": 3,
      "explanation": "Query concatenates user input directly.",
      "recommendation": "Use parameterized queries."
    }
  ]
}
```

#### ❌ Error Response

```json
{
  "error": "Gemini Error: Invalid API Key or Quota exhausted"
}
```

---

## 🛡️ Guidelines Before Use

- Make sure your `.env` file contains a **valid** Gemini API key.
- This tool does **not** execute the uploaded code — only static analysis.
- Currently supports only **text-based files** (`.py`, `.js`, `.html`, etc.)
- Avoid uploading large files (>1MB). Use chunked analysis or RAG if needed.
- This tool is for **educational and DevSecOps testing** only.

---

## 🤖 Coming Soon

- RAG-based exploit mapping using ExploitDB/CVE
- Line-by-line vulnerability highlighting
- React-based frontend dashboard

---

## 👨‍💻 Author

**Kushan Chaudhary**  
🔗 [LinkedIn](https://www.linkedin.com/in/kushan-chaudhary-77ba401a4/)  
🛠 DevSecOps • Cybersecurity • AI

---

## 📜 License

MIT License
