from shared_logic.command_pattern.analysis_command import AnalysisCommand
from model import train_and_evaluate_stock_model_with_image


class LSTMCommand(AnalysisCommand):
    def __init__(self, issuer, train_ratio=0.7, rolling_window=5,
                 n_units=50, dropout_rate=0.2, epochs=20, batch_size=32):
        self.issuer = issuer
        self.train_ratio = train_ratio
        self.rolling_window = rolling_window
        self.n_units = n_units
        self.dropout_rate = dropout_rate
        self.epochs = epochs
        self.batch_size = batch_size

    def execute(self):
        prediction, chart_base64 = train_and_evaluate_stock_model_with_image(
            stock_symbol=self.issuer,
            train_ratio=self.train_ratio,
            rolling_window=self.rolling_window,
            n_units=self.n_units,
            dropout_rate=self.dropout_rate,
            epochs=self.epochs,
            batch_size=self.batch_size
        )
        return {"prediction": prediction, "image": chart_base64, "error": None}
