from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def send_request(self, arg):
        pass
    