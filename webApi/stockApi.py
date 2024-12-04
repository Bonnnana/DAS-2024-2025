
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
# Enable CORS for all routes

# Database path
db_path = '../Homework 1/all_issuers_data.db'


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


@app.route('/issuers_data/<issuer>', methods=['GET'])
def get_issuer_data(issuer):
    conn = connect_db()
    cursor = conn.cursor()

    # Convert issuer to uppercase for case-insensitive matching
    issuer = issuer.upper()

    # SQL query to fetch all data for the specified issuer
    cursor.execute("SELECT * FROM issuers_data WHERE ISSUER = ? ORDER BY DATE DESC", (issuer,))
    rows = cursor.fetchall()  # Fetch all rows matching the issuer
    conn.close()

    if rows:
        # Add a 'line_number' to each row in the list
        result = [{"line_number": index + 1, **dict(row)} for index, row in enumerate(rows)]
        return jsonify(result)
    else:
        return jsonify({'error': 'Data not found for the specified issuer'}), 404

if __name__ == '__main__':
    app.run(debug=True)
