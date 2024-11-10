import asyncio
import sqlite3

from filters.import_all_stocks_filter import ImportAllStocksFilter
from filters.check_last_date_filter import CheckLastDateFilter
from filters.fetch_missing_data_filter import FetchDataFilter


def save_to_database(data, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for issuer_data in data:
            for entry in issuer_data:
                cursor.execute('''
                    INSERT OR IGNORE INTO issuers_data (
                        ISSUER, DATE, LAST_TRADE_PRICE, MAX_PRICE, MIN_PRICE, AVG_PRICE,
                        PERCENT_CHANGE, VOLUME, TURNOVER, TOTAL_TURNOVER
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    entry['issuer'], entry['date'], entry['last_trade_price'], entry['max_price'],
                    entry['min_price'], entry['avg_price'], entry['percent_change'],
                    entry['volume'], entry['turnover'], entry['total_turnover']
                ))
        conn.commit()


def run_pipeline(db_path):

    filters = [
        ImportAllStocksFilter(),
        CheckLastDateFilter(db_path),
        FetchDataFilter()
    ]

    data = None  # Nema pocetna vrednost

    for filter_instance in filters:
        # za FetchDataFilter imame asyncio izvrsuvanje
        if isinstance(filter_instance, FetchDataFilter):
            data = asyncio.run(filter_instance.process(data))
        else:
            data = filter_instance.process(data)

    save_to_database(data, db_path)
