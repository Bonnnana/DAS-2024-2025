from analysis_command import AnalysisCommand
from model import train_and_evaluate_stock_model_with_image

class LSTMCommand(AnalysisCommand):
    """
    A concrete command that executes your XGBoost-based model analysis.
    """

    def __init__(self, issuer, train_ratio=0.8, rolling_window=5,
                 n_estimators=100, max_depth=3, learning_rate=0.1):
        self.issuer = issuer
        self.train_ratio = train_ratio
        self.rolling_window = rolling_window
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate

    def execute(self):
        prediction, chart_base64 = train_and_evaluate_stock_model_with_image(
            stock_symbol=self.issuer,
            train_ratio=self.train_ratio,
            rolling_window=self.rolling_window,
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            learning_rate=self.learning_rate
        )
        return {"prediction": prediction, "image": chart_base64,"error": None,}