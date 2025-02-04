from typing import Generator
from app.core.llm_client_interface import LLMClientInterface


class ChatClient:
    def __init__(self, llm_client: LLMClientInterface):
        self.llm_client = llm_client

    def send_request(self, request_data) -> Generator[bytes, None, None]:
        return self.llm_client.send_request(request_data)
    