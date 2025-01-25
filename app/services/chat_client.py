from app.core.ollama_client import OllamaClient


class ChatClient:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def send_request(self, request_data):
        response = self.ollama_client.completion_stream(request_data)
        return response
    