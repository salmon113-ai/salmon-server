import aiohttp
import json
from typing import AsyncGenerator
import logging
import requests

# 로거 설정 TODO:: 로그가 콘솔에 남지 않는 증상 확인
logger = logging.getLogger('ollama_client')
logger.setLevel(logging.DEBUG)

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

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
            "stream": True
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
                        print(line)
                        json_response = json.loads(line)
                        yield json_response
                        
                        # Check if response is done
                        if json_response.get("done", False):
                            break
                            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
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
        
        # Prepare the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True
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
                        print(line)
                        # Parse JSON response
                        json_response = json.loads(line)
                        
                        # Check if response is done
                        if json_response.get("done", False):    
                            break

                        yield json_response.get("response", "")

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise
            