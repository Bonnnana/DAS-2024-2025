"""
    Flask application to fetch and serve the most liquid stocks data on Macedonian Stock Exchange.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from most_liquid import most_liquid_scrape

app = Flask(__name__)
CORS(app)


@app.route('/mostLiquid', methods=['GET'])
def get_most_liquid():
    try:
        data = most_liquid_scrape()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5005, debug=True)
