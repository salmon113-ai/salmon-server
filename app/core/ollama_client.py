import aiohttp
from typing import AsyncGenerator

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def generate_stream(self, message: str) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": "llama2",
                    "prompt": message,
                    "stream": True
                }
            ) as response:
                async for line in response.content:
                    if line:
                        yield line.decode().strip()