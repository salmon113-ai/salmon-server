import aiohttp
import json
from typing import AsyncGenerator
import requests



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
                        response_data = line.decode("utf-8")

                        print(f"Response: {response_data}")

                        json_response = json.loads(response_data)
                                                
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
        # payload = {
        #     "model": model,
        #     "prompt": prompt,
        #     "stream": True
        # }
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
            with requests.post(self.base_url + "/api/generate", json=payload, headers=headers, stream=True) as response:
            # with requests.post(self.base_url + "/v1/chat/completions", json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()  # Raise exception for bad status codes
                
                # Process the streaming response
                for line in response.iter_lines():
                    if line:
                        # Parse JSON response
                        response_data = line.decode("utf-8")

                        print(f"Response: {response_data}")

                        json_response = json.loads(response_data)
                        
                        # Check if response is done
                        if json_response.get("done", False):
                            break

                        yield json_response.get("content", "")

        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise
            