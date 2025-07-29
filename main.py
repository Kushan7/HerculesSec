from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.scan import router as scan_router

app = FastAPI(
    title="Hercules Secure",
    description="AI-powered vulnerability scanner for MERN stack and low-code websites",
    version="0.1.0",
)

# CORS config (optional but helpful during local dev with frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount your API router
app.include_router(scan_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Hercules Secure 🛡️"}
