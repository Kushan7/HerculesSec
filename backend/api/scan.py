from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import tempfile

from backend.scanner.analyze import analyze_code_with_llm

router = APIRouter()

@router.post("/scan")
async def scan_code(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Analyze the file using LLM
        result = analyze_code_with_llm(tmp_path)

        # Clean up
        os.remove(tmp_path)

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to process file: {str(e)}"}
        )
