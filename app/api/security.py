"""
API security layer with rate limiting and auth
"""
from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
import os

limiter = Limiter(key_func=get_remote_address)

async def verify_api_key(request: Request):
    """Validate X-API-Key header"""
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=401, 
            detail="Invalid API credentials"
        ) 