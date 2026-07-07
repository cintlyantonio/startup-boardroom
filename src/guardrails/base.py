from abc import ABC, abstractmethod

class Guardrail(ABC):
    @abstractmethod
    def check(self, output: str) -> bool:
        pass
