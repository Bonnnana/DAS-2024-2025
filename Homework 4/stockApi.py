"""
    Flask application that serves as a centralized entry point for interacting with multiple
    microservices related to stock analysis.
"""

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Microservice URLs
SCRAPING_SERVICE_URL = "http://localhost:5001"
TECHNICAL_ANALYSIS_SERVICE_URL = "http://localhost:5002"
FUNDAMENTAL_ANALYSIS_SERVICE_URL = "http://localhost:5003"
LSTM_MODEL_SERVICE_URL = "http://localhost:5004"
MOST_LIQUID_SERVICE_URL = "http://localhost:5005"


@app.route('/scrape-historical-data', methods=['POST'])
def run_scraping_pipeline():
    try:
        response = requests.post(f"{SCRAPING_SERVICE_URL}/scrape-historical-data")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data', methods=['GET'])
def get_issuers_data():
    try:
        response = requests.get(f"{SCRAPING_SERVICE_URL}/issuers_data")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data/<issuer>', methods=['GET'])
def get_issuer_data(issuer):
    try:
        params = request.args  # Pass query parameters (startDate, endDate)
        response = requests.get(f"{SCRAPING_SERVICE_URL}/issuers_data/{issuer}", params=params)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/mostLiquid', methods=['GET'])
def get_most_liquid():
    try:
        response = requests.get(f"{MOST_LIQUID_SERVICE_URL}/mostLiquid")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data/<issuer>/predict', methods=['GET'])
def prediction(issuer):
    try:
        params = request.args
        response = requests.get(f"{LSTM_MODEL_SERVICE_URL}/issuers_data/{issuer}/predict", params=params)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data/<issuer>/technical', methods=['GET'])
def technical_analysis(issuer):
    try:
        timeperiod = request.args.get('days', default=30, type=int)
        data = {"issuer": issuer, "timeperiod": timeperiod}
        response = requests.post(f"{TECHNICAL_ANALYSIS_SERVICE_URL}/technical", json=data)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data/<issuer>/fundamental', methods=['GET'])
def fundamental_analysis(issuer):
    try:
        response = requests.get(f"{FUNDAMENTAL_ANALYSIS_SERVICE_URL}/issuers_data/{issuer}/fundamental")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Initializing and running pipeline via scraping service...")
    try:
        response = requests.post(f"{SCRAPING_SERVICE_URL}/scrape-historical-data")
        if response.status_code == 200:
            print("Pipeline executed successfully:", response.json()["message"])
        else:
            print("Pipeline execution failed:", response.json())
    except requests.RequestException as e:
        print(f"Error initializing database and running pipeline: {e}")

    app.run(debug=True)
