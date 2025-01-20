import aiohttp
import json
from typing import AsyncGenerator
import logging

# 로거 설정 TODO:: 로그가 콘솔에 남지 않는 증상 확인
logger = logging.getLogger('ollama_client')
logger.setLevel(logging.DEBUG)

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def generate_stream(self, message: str) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": "llama3.1:latest",
                        "prompt": message,
                        "stream": True
                    }
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API 호출 실패: {response.status} - {error_text}")
                    
                    async for line in response.content:
                        if line:
                            try:
                                json_response = json.loads(line)

                                # logger.log(logging.INFO, f"JSON 응답: {json_response}")

                                # print(f"JSON 응답: {json_response}")

                                if 'response' in json_response:
                                    yield json_response['response']
                                if json_response.get('done', False):
                                    break
                            except json.JSONDecodeError as e:
                                print(f"JSON 파싱 에러: {e}")
                                continue
            
            except aiohttp.ClientError as e:
                raise Exception(f"네트워크 오류: {str(e)}")
            