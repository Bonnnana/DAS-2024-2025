"""
    FILTER 2
"""

from datetime import datetime, timedelta
from typing import List
from .base_filter import Filter


class CheckLastDateFilter(Filter):
    def __init__(self, connection):
        self.connection = connection

    def get_last_available_date(self, issuer_code: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(DATE) FROM issuers_data WHERE ISSUER = ?", (issuer_code,))
            result = cursor.fetchone()

            return result[0] if result else None
        except Exception as e:
            return None

    def process(self, issuers: List[str]) -> List[dict]:
        date_for_issuer = []
        for issuer in issuers:
            last_date = self.get_last_available_date(issuer)

            if last_date is None:
                date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')
                date_for_issuer.append({
                    "issuer": issuer,
                    "last_date": date
                })
            else:
                date_for_issuer.append({
                    "issuer": issuer,
                    "last_date": last_date
                })

        return date_for_issuer
