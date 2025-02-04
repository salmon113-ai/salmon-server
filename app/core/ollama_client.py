import asyncio
import json
from typing import Generator
import requests

from app.core.llm_client_interface import LLMClientInterface
from ..utils.logger import get_logger, log_function_call

logger = get_logger(__name__)

# OllamaClient class inherits from LLMClient
class OllamaClient(LLMClientInterface):
    def __init__(self, base_url: str = "http://localhost:11434", model="llama3.1:latest", stream: bool = False):
        self.base_url = base_url
        self.stream = stream
        self.logger = logger
        self.model = model

    @log_function_call(logger)
    def send_request(self, prompt) -> Generator[bytes, None, None]:

        request_data = prompt

        payload = {
                "model": self.model,
                "messages": request_data.get("messages", []),
                "stream": request_data.get("stream", True),
            }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # Send POST request with streaming enabled
            with requests.post(self.base_url + "/v1/chat/completions", json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()  # Raise exception for bad status codes
                
                # Process the streaming response
                for line in response.iter_lines():
                    if line:
                        self.logger.debug(f"Response: {line}")
                        
                        yield line + b'\n'

        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama 접속 오류: {e}")
            yield b'Ollama connection error.' + b'\n'
 
            