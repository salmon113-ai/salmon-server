from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import aiohttp
from typing import AsyncGenerator
# import logging
# from sys import stdout

# logger = logging.getLogger('rag_pipeline')
# logger.setLevel(logging.DEBUG)

class RagClient:
    def __init__(self, base_url: str = "http://host.docker.internal:8080"):
        self.base_url = base_url

    async def generate_stream(self, message: str) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/stream/chat",
                json={
                    "message": message
                }
            ) as response:
                async for line in response.content:
                    if line:
                        yield line.decode().strip()


class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "pipeline_example"

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

        print(f"{__name__} inlet body: {body}")
        print(f"{__name__} inlet user: {user}")

        return body

    async def outlet(self, body: dict, user: dict) -> dict:
        # This function is called after the OpenAI API response is completed. You can modify the messages after they are received from the OpenAI API.

        print(f"{__name__} outlet body: {body}")
        print(f"{__name__} outlet user: {user}")

        return body

    # def pipe(
    #     self, user_message: str, model_id: str, messages: List[dict], body: dict
    # ) -> Union[str, Generator, Iterator]:
    #     # This is where you can add your custom pipelines like RAG.
    #     print(f"pipe:{__name__}")

    #     # If you'd like to check for title generation, you can add the following check
    #     if body.get("title", False):
    #         print("Title Generation Request")

    #     print(f"pipe:{__name__} model_id: {model_id}")
    #     print(f"pipe:{__name__} message: {messages}")
    #     print(f"pipe:{__name__} user_message: {user_message}")
    #     print(f"pipe:{__name__} body: {body}")

    #     # send to rag application server
    #     ragClient = RagClient()

    #     print(ragClient.base_url)

    #     ragClient.generate_stream(user_message)

    #     return "Hello, World!"   

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.rag_client.generate_stream(user_message):
            yield chunk 
