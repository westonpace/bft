from abc import ABC, abstractmethod

from .types import Case


class CaseRunner(ABC):
    @abstractmethod
    def run_case(self, case: Case) -> bool:
        raise NotImplementedError()
