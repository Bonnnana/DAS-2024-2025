import sqlite3


def initialize_database(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute('''
               CREATE TABLE IF NOT EXISTS issuers_data ( 
                   ISSUER TEXT NOT NULL,
                   DATE DATE NOT NULL ,
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
