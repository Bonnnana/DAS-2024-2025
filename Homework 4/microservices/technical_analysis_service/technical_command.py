from shared_logic.command_pattern.analysis_command import AnalysisCommand
from tech_analysis import perform_technical_analysis


class TechnicalAnalysisCommand(AnalysisCommand):
    def __init__(self, db_conn, issuer, timeperiod=30):
        self.db_conn = db_conn
        self.issuer = issuer
        self.timeperiod = timeperiod

    def execute(self):
        result = perform_technical_analysis(self.db_conn, self.issuer, self.timeperiod)
        return result
