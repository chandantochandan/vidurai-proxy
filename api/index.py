"""
Vercel serverless function entry point
Wraps FastAPI app with Mangum for AWS Lambda compatibility
"""
from mangum import Mangum
from src.main import app

# Export handler for Vercel
handler = Mangum(app)
