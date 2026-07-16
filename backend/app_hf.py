"""
RiskShield-BFSI-X - Hugging Face Spaces Deployment Wrapper
This file wraps the FastAPI app for Hugging Face Spaces compatibility
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the main app
from app import app as fastapi_app

# Hugging Face Spaces specifics
HF_SPACE_ID = os.getenv("SPACE_ID", "unknown")
HF_SPACE_HOST = os.getenv("HF_SPACE_HOST", "localhost")
HF_SPACE_PORT = int(os.getenv("HF_SPACE_PORT", 7860))

# Update CORS for Hugging Face Spaces
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://huggingface.co",
        "https://*.hf.space",
        "http://localhost:7860",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a Hugging Face-specific info endpoint
@fastapi_app.get("/hf-info")
async def hf_info():
    """Hugging Face Spaces info endpoint"""
    return {
        "space_id": HF_SPACE_ID,
        "space_host": HF_SPACE_HOST,
        "space_port": HF_SPACE_PORT,
        "deployment": "hugging_face_spaces",
        "app": "RiskShield-BFSI-X"
    }

# Export app for Hugging Face
app = fastapi_app
