"""
    Flask application for collecting news data
    and performing fundamental analysis for specific issuers.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from shared_logic.command_pattern.analysis_invoker import AnalysisInvoker
from fundamental_command import FundamentalAnalysisCommand
from collecting_news_data import retrieve_data


app = Flask(__name__)
CORS(app)

analysis_invoker = AnalysisInvoker()

NEWS_DATA_FILE = "news_data.csv"
SENTIMENT_DATA_FILE = "news_sentiment_data.csv"


@app.route('/collect-news-data', methods=['POST'])
def collect_news_data():
    try:
        retrieve_data()
        return jsonify({"message": "News data collection completed successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data/<issuer>/fundamental', methods=['GET'])
def fundamental_analysis(issuer):
    try:
        cmd = FundamentalAnalysisCommand(company_code=issuer)

        result = analysis_invoker.execute_command(cmd)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    if not os.path.exists(NEWS_DATA_FILE):
        print(f"News data file '{NEWS_DATA_FILE}' not found. Please run the news data collection process.")
    if not os.path.exists(SENTIMENT_DATA_FILE):
        print(f"Sentiment data file '{SENTIMENT_DATA_FILE}' not found. Sentiment analysis will create it as needed.")

    app.run(port=5003, debug=True)
