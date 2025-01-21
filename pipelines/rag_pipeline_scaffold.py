from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import aiohttp
import json
from typing import AsyncGenerator
import requests
# import logging
# from sys import stdout

# logger = logging.getLogger('rag_pipeline')
# logger.setLevel(logging.DEBUG)

class RagClient:
    def __init__(self, base_url: str = "http://host.docker.internal:8080"):
        self.base_url = base_url

    # async def generate_stream(self, message: str) -> AsyncGenerator[str, None]:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(
    #             f"{self.base_url}/stream/chat",
    #             json={
    #                 "message": message
    #             }
    #         ) as response:
    #             async for line in response.content:
    #                 if line:
    #                     yield line.decode().strip()
    
    def generate_stream(self, message: str):
        
        # Prepare the request payload
        payload = {
            "message": message
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # Send POST request with streaming enabled
            with requests.post(self.base_url + "/stream/chat", json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()  # Raise exception for bad status codes
                
                # Process the streaming response
                # for line in response.iter_lines():
                #     if line:
                #         # Parse JSON response
                #         json_response = json.loads(line)
                #         yield json_response.get("response", "")
                        
                #         # Check if response is done
                #         if json_response.get("done", False):
                #             break

                return response.iter_lines()
                            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise
            

class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        # The name of the pipeline.
        self.name = "Pipeline Rag"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    async def on_valves_updated(self):
        # This function is called when the valves are updated.
        pass

    async def inlet(self, body: dict, user: dict) -> dict:
        # This function is called before the OpenAI API request is made. You can modify the form data before it is sent to the OpenAI API.
        return body

    async def outlet(self, body: dict, user: dict) -> dict:
        # This function is called after the OpenAI API response is completed. You can modify the messages after they are received from the OpenAI API.
        return body

    # 샘플 데이터
    users = [
        {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 25, "city": "San Francisco"},
        {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"}
    ]

    # NDJSON 데이터 생성기
    def generate_ndjson(self) -> Generator[str, None, None]:
        for user in self.users:
            yield json.dumps(user) + "\n"  # JSON 문자열로 변환 후 줄바꿈 추가

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        
        payload = {
            "message": user_message
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # Send POST request with streaming enabled
            with requests.post("http://host.docker.internal:8080" + "/stream/chat", json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()  # Raise exception for bad status codes
                
                # Process the streaming response
                # for line in response.iter_lines():
                #     if line:
                #         # Parse JSON response
                #         json_response = json.loads(line)
                #         yield json_response.get("response", "")
                        
                #         # Check if response is done
                #         if json_response.get("done", False):
                #             break

                return response.iter_lines()
                            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise
    