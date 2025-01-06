from analysis_command import AnalysisCommand

class AnalysisInvoker:
    """
    The Invoker in the Command pattern.
    It can store commands, queue them, or just call them immediately.
    """

    def execute_command(self, command: AnalysisCommand):
        """
        Executes a given command's action and returns its result.
        """
        return command.execute()