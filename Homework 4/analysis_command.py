from abc import ABC, abstractmethod

class AnalysisCommand(ABC):
    """
    The Command interface, declaring the execute() method.
    Each analysis (fundamental, technical, XGBoost) will implement this.
    """

    @abstractmethod
    def execute(self):
        """
        Perform the analysis and return the results.
        """
        pass