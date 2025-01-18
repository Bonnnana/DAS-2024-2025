import asyncio
from filters.import_all_stocks_filter import ImportAllStocksFilter
from filters.check_last_date_filter import CheckLastDateFilter
from filters.fetch_missing_data_filter import FetchDataFilter


def save_to_database(data, conn):
    try:
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
    except Exception as e:
        conn.commit()


def run_pipeline(conn):
    """
    Executes a data processing pipeline to fetch, process, and save stock data.

    This pipeline consists of the following filters:
    1. `ImportAllStocksFilter`: Retrieves all stock issuers or symbols.
    2. `CheckLastDateFilter`: Identifies the most recent date for which data exists in the database.
    3. `FetchDataFilter`: Fetches any missing stock data asynchronously.

    Args:
        conn (sqlite3.Connection): The database connection object used to query and save data.

    Returns:
        None: This function does not return a value. It processes and saves data directly to the database.
    """

    filters = [
        ImportAllStocksFilter(),
        CheckLastDateFilter(conn),
        FetchDataFilter()
    ]

    data = None

    for filter_instance in filters:
        if isinstance(filter_instance, FetchDataFilter):
            data = asyncio.run(filter_instance.process(data))
        else:
            data = filter_instance.process(data)

    save_to_database(data, conn)


