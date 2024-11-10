"""FILTER 3"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import List

from base_filter import Filter


class FetchDataFilter(Filter):
    def __init__(self):
        self.base_url = 'https://www.mse.mk/en/stats/symbolhistory'

    async def fetch_data(self, session, issuer: str, start_date: str, end_date: str, max_retries=5) -> List[dict]:
        url = f"{self.base_url}/{issuer}"
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        rows = []
        current_start = start_date

        while current_start < end_date:
            # tabelata na stranata na mse pokazuva podatoci vo interval od samo 365 dena
            current_end = min(current_start + timedelta(days=365), end_date)

            # parametri za URL vo GET baranjeto
            params = {
                "FromDate": current_start.strftime('%m/%d/%Y'),
                "ToDate": current_end.strftime('%m/%d/%Y')
            }

            retries = 0
            while retries < max_retries:
                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 503:
                            retries += 1
                            wait_time = 2
                            print(f"503 error, retrying in {wait_time} seconds...")
                            await asyncio.sleep(wait_time)
                            continue
                        response.raise_for_status()
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        table_body = soup.find('tbody')
                        if table_body:
                            rows_in_table = table_body.find_all('tr')
                            for row in rows_in_table:
                                cells = row.find_all('td')
                                if cells:
                                    # Skokni gi redovite kade volume e 0
                                    volume = int(cells[6].text.strip().replace(",", "") or 0)

                                    if volume == 0:
                                        continue
                                    rows.append({
                                        "issuer": issuer,
                                        "date": datetime.strptime(cells[0].text.strip(), "%m/%d/%Y").strftime("%Y-%m-%d"),
                                        "last_trade_price": self.format_price(cells[1].text.strip()) or "0,00",
                                        "max_price": self.format_price(cells[2].text.strip()) or "0,00",
                                        "min_price": self.format_price(cells[3].text.strip()) or "0,00",
                                        "avg_price": self.format_price(cells[4].text.strip()) or "0,00",
                                        "percent_change": cells[5].text.strip().replace(".", ",") or "0,00",
                                        "volume": volume,
                                        "turnover": self.format_price(cells[7].text.strip()) or "0,00",
                                        "total_turnover": self.format_price(cells[8].text.strip()) or "0,00"
                                    })
                        break
                except aiohttp.ClientResponseError:
                    if retries == max_retries - 1:
                        print(f"Failed to fetch data for {issuer} after {max_retries} attempts.")
                        return []
                    retries += 1
                    wait_time = 2
                    print(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)

            # zemi go sledniot 365 dneven interval
            current_start = current_end + timedelta(days=1)

        return rows

    def format_price(self, price_str: str) -> str:
        if not price_str:
            return "0,00"

        price_str = price_str.replace(",", "").replace(".", ",")
        integer_part, _, decimal_part = price_str.partition(",")

        if not integer_part:
            integer_part = "0"
        if not decimal_part:
            decimal_part = "00"

        integer_part_formatted = f"{int(integer_part):,}".replace(",", ".")

        return f"{integer_part_formatted},{decimal_part[:2]}"

    async def process(self, issuers_with_dates: List[dict]) -> List[List[dict]]:
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_data(session, issuer_info["issuer"], issuer_info["last_date"],
                                datetime.now().strftime('%Y-%m-%d'))
                for issuer_info in issuers_with_dates
            ]
            results = await asyncio.gather(*tasks)  # gi izvrsuva site tasks konkurentno
            return list(results)
