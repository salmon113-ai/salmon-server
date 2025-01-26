import json
from typing import Generator
import requests
from ..utils.logger import get_logger, log_function_call

logger = get_logger(__name__)


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", stream: bool = False):
        self.base_url = base_url
        self.stream = stream
        self.logger = logger

    @log_function_call(logger)
    def completion_stream(self, prompt, model="llama3.1:latest") -> Generator[bytes, None, None]:
        """
        Send a streaming request to Ollama API and yield responses
        
        Args:
            prompt (str): The prompt to send to the model
            model (str): The model to use (default: llama3.1:latest)
            api_url (str): The Ollama API endpoint URL
            
        Yields:
            dict: Parsed JSON response from the API
        """

        request_data = prompt

        payload = {
                "model": model,
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
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise

            