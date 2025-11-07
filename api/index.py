"""
Vercel serverless function entry point
Wraps FastAPI app with Mangum for AWS Lambda compatibility
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from mangum import Mangum
from src.main import app

# Export handler for Vercel
handler = Mangum(app)
