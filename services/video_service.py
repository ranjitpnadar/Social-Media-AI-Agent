import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
async def generate_video(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://video-api.com/generate",
            json={"prompt": prompt}
        )
        resp.raise_for_status()
        return resp.json()["url"]