"""
    FILTER 1
"""

import requests
from bs4 import BeautifulSoup
from typing import List
from .base_filter import Filter


class ImportAllStocksFilter(Filter):
    def __init__(self):
        self.url = 'https://www.mse.mk/en/stats/symbolhistory/ADIN'

    def get_valid_issuers(self) -> List[str]:
        response = requests.get(self.url)
        response.raise_for_status()

        raw_html = response.text
        soup = BeautifulSoup(raw_html, 'html.parser')

        issuers = soup.find_all('option')

        imported_issuers = []
        for issuer in issuers:
            issuer_name = issuer.text.strip()
            if issuer_name and issuer_name.isalpha():
                imported_issuers.append(issuer_name)

        return imported_issuers

    def process(self, data) -> List[str]:
        valid_issuers = self.get_valid_issuers()
        return valid_issuers
