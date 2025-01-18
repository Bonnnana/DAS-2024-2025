from shared_logic.command_pattern.analysis_command import AnalysisCommand


class AnalysisInvoker:
    """
    The Invoker in the Command pattern.
    This class is responsible for invoking commands that follow the Command pattern.
    """

    def execute_command(self, command: AnalysisCommand):
        return command.execute()
