import requests
from bs4 import BeautifulSoup


def most_liquid_scrape():
    url = "https://www.mse.mk/mk"

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # "Најтргувани"
    table = soup.find('div', {'id': 'topSymbolValueTopSymbols'}).find('table')

    headers = [th.text.strip() for th in table.find_all('th')]

    data = []
    for row in table.find_all('tr')[1:]:  # Прескокнување на првиот ред
        cells = row.find_all('td')
        if cells:
            symbol = cells[0].text.strip()  # Шифра на акцијата
            data.append({
                "ISSUER": symbol,
                "AVG_PRICE": cells[1].text.strip(), # Min price (not available in data, use avg for now)
                "PERCENT_CHANGE": cells[2].text.strip(),
                "TOTAL_TURNOVER": cells[3].text.strip(),  # Assuming turnover data is available
            })

    return data




