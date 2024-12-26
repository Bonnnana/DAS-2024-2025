import sqlite3
import pandas as pd

db_path = '../../Homework 1/all_issuers_data.db'


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


conn = connect_db()
query = "SELECT * FROM issuers_data"

try:
    # Load data into a pandas DataFrame
    data = pd.read_sql_query(query, conn)
    print(data.head())
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()