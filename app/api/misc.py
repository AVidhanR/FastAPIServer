"""
Miscellaneous API endpoints for demonstration purposes.
"""
import asyncio
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
import httpx

from app.models import MessageResponse

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API.
    Public endpoint - no authentication required.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint.
    
    Returns a pong response for basic connectivity testing.
    Public endpoint - no authentication required.
    """
    return {"message": "pong"}


@router.get("/time")
async def get_server_time():
    """
    Get server time.
    
    Returns the current server time in various formats.
    Public endpoint - no authentication required.
    """
    now = datetime.utcnow()
    return {
        "utc": now.isoformat(),
        "unix_timestamp": int(now.timestamp()),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timezone": "UTC"
    }


@router.get("/echo")
async def echo(message: str = Query(..., description="Message to echo back")):
    """
    Echo endpoint.
    
    Returns the provided message back to the client.
    Public endpoint - no authentication required.
    """
    return {
        "original_message": message,
        "echoed_at": datetime.utcnow().isoformat(),
        "length": len(message)
    }


@router.post("/echo", response_model=MessageResponse)
async def echo_post(data: Dict[str, Any]):
    """
    Echo POST endpoint.
    
    Returns the provided JSON data back to the client.
    Public endpoint - no authentication required.
    """
    return MessageResponse(
        message=f"Received data: {data}",
        success=True
    )


@router.get("/random-quote")
async def get_random_quote():
    """
    Get a random quote.
    
    Fetches a random quote from an external API.
    Public endpoint - no authentication required.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.quotable.io/random")
            if response.status_code == 200:
                quote_data = response.json()
                return {
                    "quote": quote_data["content"],
                    "author": quote_data["author"],
                    "tags": quote_data["tags"]
                }
            else:
                # Fallback quote if API is unavailable
                return {
                    "quote": "The only way to do great work is to love what you do.",
                    "author": "Steve Jobs",
                    "tags": ["motivational"]
                }
    except Exception:
        # Fallback quote if there's any error
        return {
            "quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "author": "Winston Churchill",
            "tags": ["inspirational"]
        }


@router.get("/weather")
async def get_weather(city: str = Query(..., description="City name")):
    """
    Get weather information (demo).
    
    Returns mock weather data for the specified city.
    In production, this would integrate with a real weather API.
    Public endpoint - no authentication required.
    """
    # Mock weather data
    import random
    
    weather_conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "clear"]
    
    return {
        "city": city,
        "temperature": round(random.uniform(-10, 35), 1),
        "condition": random.choice(weather_conditions),
        "humidity": random.randint(30, 90),
        "wind_speed": round(random.uniform(0, 25), 1),
        "timestamp": datetime.utcnow().isoformat(),
        "note": "This is mock data for demo purposes"
    }


@router.get("/slow")
async def slow_endpoint(delay: int = Query(5, ge=1, le=30, description="Delay in seconds")):
    """
    Slow endpoint for testing.
    
    Simulates a slow operation by waiting for the specified number of seconds.
    Useful for testing timeout handling and loading states.
    Public endpoint - no authentication required.
    """
    await asyncio.sleep(delay)
    return {
        "message": f"Waited for {delay} seconds",
        "completed_at": datetime.utcnow().isoformat()
    }


@router.get("/error")
async def trigger_error(status_code: int = Query(500, ge=400, le=599)):
    """
    Error endpoint for testing.
    
    Triggers an HTTP error with the specified status code.
    Useful for testing error handling.
    Public endpoint - no authentication required.
    """
    error_messages = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable"
    }
    
    message = error_messages.get(status_code, "HTTP Error")
    raise HTTPException(status_code=status_code, detail=message)
