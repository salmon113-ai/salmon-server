from typing import Generator
from app.core.llm_client import LLMClient


class ChatClient:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def send_request(self, request_data) -> Generator[bytes, None, None]:
        return self.llm_client.send_request(request_data)
    