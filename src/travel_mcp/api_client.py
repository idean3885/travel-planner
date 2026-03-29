import httpx
import logging
import os
from typing import Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger("travel-mcp-server")

# 환경변수는 모듈 로드 시 읽되, Claude Desktop의 env 블록으로 주입된 값도 반영됨
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "booking-com15.p.rapidapi.com")


async def make_rapidapi_request(endpoint: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Make a request to the RapidAPI with proper error handling."""
    # 런타임에 환경변수 재확인 (Claude Desktop env 블록 지원)
    api_key = RAPIDAPI_KEY or os.getenv("RAPIDAPI_KEY")
    api_host = RAPIDAPI_HOST or os.getenv("RAPIDAPI_HOST", "booking-com15.p.rapidapi.com")

    if not api_key:
        return {"error": "RAPIDAPI_KEY is not set. Please check your .env file or environment variables."}

    url = f"https://{api_host}{endpoint}"

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }

    logger.info(f"Making API request to {endpoint} with params: {params}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            logger.info(f"API request to {endpoint} successful")
            return response.json()
        except Exception as e:
            logger.error(f"API request to {endpoint} failed: {str(e)}")
            return {"error": str(e)}
