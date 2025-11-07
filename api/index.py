"""
Vercel FastAPI Handler
Vercel's Python runtime handles ASGI apps directly - no Mangum needed!
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app - Vercel will automatically detect and serve it
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
        "mode": "vercel-native"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "vidurai-proxy",
        "version": "1.1.0"
    }
