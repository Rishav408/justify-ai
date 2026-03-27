from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.api.routes import router

app = FastAPI(title="Justify-AI Backend", version="1.5")

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Analysis Routes
app.include_router(router, prefix="/api")

# Serve the Frontend statically (so you can run the UI from the same server)
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True))

if __name__ == "__main__":
    print("=========================================")
    print(" STYLLABUS MODE - JUSTIFY-AI STARTING")
    print("=========================================")
    uvicorn.run(app, host="127.0.0.1", port=8000)
