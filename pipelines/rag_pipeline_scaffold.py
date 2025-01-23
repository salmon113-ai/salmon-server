from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import json
import requests

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

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        
        if body.get("title", False):
            print("Title Generation")
            return "Pipeline Rag"
        
        headers = {
            "Content-Type": "application/json"
        }

        print(f"message: {messages}")
        print(f"body: {body}")
        
        # with 절을 사용하면 openwebui에서 정상적으로 메시지를 못가져감. 메시지 몇개 가져가고 통신이 끊김
        try:
            r = requests.post("http://host.docker.internal:8080" + "/stream/chat", json=body, headers=headers, stream=True)
            r.raise_for_status()

            if body.get("stream", True):
                return r.iter_lines()                
            else:
                # stream 이 아닌 경우 본문을 반환해야 요약이 제대로 표시됨
                return r.content
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            raise
    