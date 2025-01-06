from analysis_command import AnalysisCommand

# Import the modules/functions you need
from fundamental_analysis import (
    process_data_in_batches,
    get_company_signal_with_percentages
)



class FundamentalAnalysisCommand(AnalysisCommand):
    """
    A concrete command that executes Fundamental (sentiment) analysis.
    """

    def __init__(self, input_csv, output_csv, company_code):
        # Store parameters needed to run the analysis
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.company_code = company_code


    def execute(self):
        # 1) Process data with your chosen strategy
        sentiment_df = process_data_in_batches(
            input_file=self.input_csv,
            output_file=self.output_csv,
            classifier_model="yiyanghkust/finbert-tone",
            batch_size=32
        )
        # 2) Generate final results or signal
        result = get_company_signal_with_percentages(sentiment_df, self.company_code)
        return result