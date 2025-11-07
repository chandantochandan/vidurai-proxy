"""
Simplified Vercel Handler
Minimal version for debugging
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Create minimal FastAPI app
app = FastAPI(
    title="Vidurai Proxy Server",
    description="Universal AI Memory Management Proxy",
    version="1.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Vidurai Proxy Server",
        "version": "1.1.0",
        "status": "running",
        "mode": "serverless-minimal"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "vidurai-proxy",
        "version": "1.1.0"
    }

# Vercel handler
handler = Mangum(app)
