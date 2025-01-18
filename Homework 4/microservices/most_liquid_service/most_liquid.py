import requests
from bs4 import BeautifulSoup


def most_liquid_scrape():
    """
    Scrapes the most liquid stocks data from the Macedonian Stock Exchange website.

    Returns:
        list: A list of dictionaries, where each dictionary contains details of a single stock.
    """

    url = "https://www.mse.mk/mk"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('div', {'id': 'topSymbolValueTopSymbols'}).find('table')

    data = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if cells:
            symbol = cells[0].text.strip()
            data.append({
                "ISSUER": symbol,
                "AVG_PRICE": cells[1].text.strip(),
                "PERCENT_CHANGE": cells[2].text.strip(),
                "TOTAL_TURNOVER": cells[3].text.strip(),
            })

    return data
