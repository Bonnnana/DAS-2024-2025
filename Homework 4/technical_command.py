from analysis_command import AnalysisCommand
import sqlite3
from tech_analysis import perform_technical_analysis

class TechnicalAnalysisCommand(AnalysisCommand):
    """
    A concrete command that executes Technical analysis (ta-lib).
    """

    def __init__(self, db_conn, issuer, timeperiod=30):
        self.db_conn = db_conn
        self.issuer = issuer
        self.timeperiod = timeperiod

    def execute(self):
        # For example, open DB, run the analysis, then close DB
        result = perform_technical_analysis(self.db_conn, self.issuer, self.timeperiod)
        return result