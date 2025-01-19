"""
    Flask application for LSTM-based stock price prediction.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from lstm_command import LSTMCommand
from shared_logic.command_pattern.analysis_invoker import AnalysisInvoker

app = Flask(__name__)
CORS(app)

analysis_invoker = AnalysisInvoker()


@app.route('/issuers_data/<issuer>/predict', methods=['GET'])
def prediction(issuer):
    try:
        train_ratio = float(request.args.get('train_ratio', 0.8))
        rolling_window = int(request.args.get('rolling_window', 5))

        cmd = LSTMCommand(issuer=issuer, train_ratio=train_ratio, rolling_window=rolling_window)
        result = analysis_invoker.execute_command(cmd)

        if result.get("error"):
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
