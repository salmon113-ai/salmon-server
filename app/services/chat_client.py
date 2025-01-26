from typing import Generator
from app.core.ollama_client import OllamaClient


class ChatClient:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def send_request(self, request_data) -> Generator[bytes, None, None]:
        return self.ollama_client.completion_stream(request_data)
    