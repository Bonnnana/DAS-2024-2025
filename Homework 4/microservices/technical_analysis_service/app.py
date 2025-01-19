"""
    Flask application to perform technical analysis for a specific stock issuer.
"""

from flask import Flask, jsonify, request
from shared_logic.command_pattern.analysis_invoker import AnalysisInvoker
from shared_logic.database.db_connection import DatabaseConnection
from technical_command import TechnicalAnalysisCommand

analysis_invoker = AnalysisInvoker()
app = Flask(__name__)


@app.route('/technical', methods=['POST'])
def perform_technical():
    try:
        data = request.json
        issuer = data.get('issuer')
        timeperiod = data.get('timeperiod', 30)

        if not issuer:
            return jsonify({"error": "Issuer is required"}), 400

        db_instance = DatabaseConnection()
        conn = db_instance.get_connection()
        if not conn:
            return jsonify({"error": "Unable to connect to the database"}), 500

        cmd = TechnicalAnalysisCommand(conn, issuer, timeperiod)
        result = analysis_invoker.execute_command(cmd)
        conn.close()
        return jsonify(result), 200

    except Exception as e:
        print(f"Error in /technical endpoint: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
