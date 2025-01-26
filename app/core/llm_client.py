from abc import ABC, abstractmethod
from typing import Generator

# Abstract class for LLM client
class LLMClient(ABC):

    # Send a request to the LLM model and yield responses
    @abstractmethod
    def send_request(self, arg) -> Generator[bytes, None, None]:
        pass
    