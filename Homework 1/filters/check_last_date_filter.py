"""FILTER 2"""

import sqlite3
from datetime import datetime, timedelta
from typing import List
from filters.base_filter import Filter


class CheckLastDateFilter(Filter):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_last_available_date(self, issuer_code: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # selekcija na posledniot datum za izdavac praten preku issuer_code
            cursor.execute("SELECT MAX(DATE) FROM issuers_data WHERE ISSUER = ?", (issuer_code,))
            result = cursor.fetchone()  # se vrakja rezultatot kako tuple (single row)
        return result[0] if result else None

    def process(self, issuers: List[str]) -> List[dict]:
        date_for_issuer = []
        for issuer in issuers:
            last_date = self.get_last_available_date(issuer)

            if last_date is None:
                # Nema podatoci vo bazata - zemi go datumot za poslednite 10 god.
                date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
                date_for_issuer.append({
                    "issuer": issuer,
                    "last_date": date
                })
            else:
                # ima podatoci - zemi go datumot do kade se vneseni podatocite
                date_for_issuer.append({
                    "issuer": issuer,
                    "last_date": last_date
                })

        return date_for_issuer

