import sys
import os

current_dir = os.path.dirname(__file__)  # directory of stockApi.py
homework1_dir = os.path.join(current_dir, '..', 'Homework 1')  # or 'Homework1'
homework1_dir = os.path.abspath(homework1_dir)

# Add "Homework 1" folder to sys.path so Python can find model.py, pipeline.py, etc.
sys.path.append(homework1_dir)
# Now import the 'main' function from main.py
from most_liquid import most_liquid_scrape
# from model import train_and_evaluate_stock_model_with_image
# from tech_analysis import perform_technical_analysis
# from fundamental_analysis import get_fundamental_analysis
# from pipeline import run_pipeline
from analysis_invoker import AnalysisInvoker
from lstm_command import LSTMCommand
from technical_command import TechnicalAnalysisCommand
from fundamental_command import FundamentalAnalysisCommand

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)
# Enable CORS for all routes

# Database path
db_path = '../../proekt/Homework 1/all_issuers_data.db'
analysis_invoker = AnalysisInvoker()


# Function to connect to the SQLite database
def connect_db():

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enables column name-based access
        print("Database connection established successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


# Route to fetch all unique issuers data
@app.route('/issuers_data', methods=['GET'])
def get_issuers_data():
    conn = connect_db()
    cursor = conn.cursor()

    # SQL query to select unique ISSUER names
    cursor.execute("SELECT DISTINCT ISSUER FROM issuers_data")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to a list of issuer names
    issuers = [row['ISSUER'] for row in rows]
    return jsonify(issuers)

@app.route('/mostLiquid', methods=['GET'])
def get_most_liquid():
    try:
        data = most_liquid_scrape()  # Call the most_liquid function
        return jsonify(data)  # Return the data as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/issuers_data/<issuer>', methods=['GET'])
def get_issuer_data(issuer):
    conn = connect_db()
    cursor = conn.cursor()

    # Convert issuer to uppercase for case-insensitive matching
    issuer = issuer.upper()

    # Extract query parameters
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    # Build the SQL query
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

    # Execute the query
    cursor.execute(query, params)
    rows = cursor.fetchall()  # Fetch all rows matching the query
    conn.close()

    if rows:
        # Add a 'line_number' to each row in the list
        result = [{"line_number": index + 1, **dict(row)} for index, row in enumerate(rows)]
        return jsonify(result)
    else:
        return jsonify({'error': 'No data found for the specified issuer'}), 404

@app.route('/issuers_data/<issuer>/predict', methods=['GET'])
def prediction(issuer):
    try:
        cmd = LSTMCommand(issuer)
        result = analysis_invoker.execute_command(cmd)

        if result.get("error") == "500":
            return jsonify(result), 500
        else:
            return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "500", "message": str(e)}), 500


@app.route('/issuers_data/<issuer>/technical', methods=['GET'])
def issuers_technical_data(issuer):
    """
    Example:
      GET /issuers_data/XYZ/technical?days=30
    """
    # Get 'days' from query params; default to 30 if not provided
    days = request.args.get('days', default=30, type=int)

    # Connect to the database
    conn = connect_db()
    if not conn:
        return jsonify({"error": "Unable to connect to the database"}), 500

    try:
        # Run your analysis function
        cmd = TechnicalAnalysisCommand(conn,issuer, days)
        result = analysis_invoker.execute_command(cmd)
        # Return the data as JSON
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Always close the database connection
        conn.close()

@app.route('/issuers_data/<issuer>/fundamental', methods=['GET'])
def fundamental(issuer):
    try:
        cmd = FundamentalAnalysisCommand("news_data.csv","news_sentiment_data.csv",issuer)
        result = analysis_invoker.execute_command(cmd)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # run_pipeline("../Homework 1/all_issuers_data.db")
    app.run(debug=True)

