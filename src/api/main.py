import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import GEMINI_API_KEY
from src.api.routes import router

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable is not set. Failing fast.", file=sys.stderr)
    sys.exit(1)

app = FastAPI(title="Startup Simulator API")

# WARNING: CORS is currently permissive for local development. 
# This must be restricted to specific frontend origins before deploying to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
