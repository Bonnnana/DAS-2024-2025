from abc import ABC, abstractmethod


class AnalysisCommand(ABC):
    """
    The Command interface, declaring the execute() method.
    Each analysis (fundamental, technical, LSTM) will implement this.
    """

    @abstractmethod
    def execute(self):
        pass
