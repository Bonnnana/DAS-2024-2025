from shared_logic.command_pattern.analysis_command import AnalysisCommand
from fundamental_analysis import get_fundamental_analysis


class FundamentalAnalysisCommand(AnalysisCommand):
    def __init__(self, company_code):
        self.company_code = company_code

    def execute(self):
        result = get_fundamental_analysis(self.company_code)
        return result
