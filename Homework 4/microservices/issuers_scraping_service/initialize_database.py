import sqlite3


def initialize_database(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS issuers_data (
                    ISSUER TEXT NOT NULL,
                    DATE DATE NOT NULL,
                    LAST_TRADE_PRICE TEXT,
                    MAX_PRICE TEXT,
                    MIN_PRICE TEXT,
                    AVG_PRICE TEXT,
                    PERCENT_CHANGE TEXT,
                    VOLUME INTEGER,
                    TURNOVER TEXT,
                    TOTAL_TURNOVER TEXT,
                    PRIMARY KEY (ISSUER, DATE)
                );
            ''')
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")
