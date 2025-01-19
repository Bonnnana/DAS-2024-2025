"""
    Flask application for managing and processing stock issuer data.
"""

from flask import Flask, jsonify, request
from initialize_database import initialize_database
from data_pipeline import run_pipeline
from shared_logic.database.db_connection import DatabaseConnection

app = Flask(__name__)


@app.route('/scrape-historical-data', methods=['POST'])
def run_data_pipeline():
    try:
        db_instance = DatabaseConnection()
        connection = db_instance.get_connection()
        initialize_database(connection)
        run_pipeline(connection)
        return jsonify({"message": "Pipeline executed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data', methods=['GET'])
def get_issuers_data():
    try:
        db_instance = DatabaseConnection()
        connection = db_instance.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT ISSUER FROM issuers_data")
        rows = cursor.fetchall()

        db_instance.close_connection()

        issuers = [row["ISSUER"] for row in rows]
        return jsonify(issuers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/issuers_data/<issuer>', methods=['GET'])
def get_issuer_data(issuer):
    try:
        db_instance = DatabaseConnection()
        connection = db_instance.get_connection()
        cursor = connection.cursor()

        issuer = issuer.upper()

        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')

        if start_date and end_date:
            query = """
                SELECT * FROM issuers_data
                WHERE ISSUER = ? AND DATE BETWEEN ? AND ?
                ORDER BY DATE DESC
            """
            params = [issuer, start_date, end_date]
        else:
            query = """
                SELECT * FROM issuers_data
                WHERE ISSUER = ?
                ORDER BY DATE DESC
            """
            params = [issuer]

        cursor.execute(query, params)
        rows = cursor.fetchall()
        db_instance.close_connection()

        if rows:
            result = [dict(row) for row in rows]
            return jsonify(result), 200
        else:
            return jsonify({"error": "No data found for the specified issuer"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
