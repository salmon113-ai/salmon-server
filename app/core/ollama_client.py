import aiohttp
import json
from typing import AsyncGenerator
import requests
from ..utils.logger import get_logger, log_function_call

logger = get_logger(__name__)


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", stream: bool = False):
        self.base_url = base_url
        self.stream = stream
        self.logger = logger

    @log_function_call(logger)
    def generate_stream(self, prompt, model="llama3.1:latest"):
        """
        Send a streaming request to Ollama API and yield responses
        
        Args:
            prompt (str): The prompt to send to the model
            model (str): The model to use (default: llama3.1:latest)
            api_url (str): The Ollama API endpoint URL
            
        Yields:
            dict: Parsed JSON response from the API
        """
        
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": self.stream
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # Send POST request with streaming enabled
            with requests.post(self.base_url + "/api/generate", json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()  # Raise exception for bad status codes
                
                # Process the streaming response
                for line in response.iter_lines():
                    if line:
                        # Parse JSON response
                        self.logger.info(f"Response: {line}")
                        yield line
                            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON response: {e}")
            raise

    def completion_stream(self, prompt, model="llama3.1:latest"):
        """
        Send a streaming request to Ollama API and yield responses
        
        Args:
            prompt (str): The prompt to send to the model
            model (str): The model to use (default: llama3.1:latest)
            api_url (str): The Ollama API endpoint URL
            
        Yields:
            dict: Parsed JSON response from the API
        """
 
        payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an agent of the AppleScript Pipeline. You have the power to control the volume of the system.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "stream": True,
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
                        self.logger.info(f"Response: {line}")
                        
                        yield line

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise
            