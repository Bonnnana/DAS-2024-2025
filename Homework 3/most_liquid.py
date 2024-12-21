import requests
from bs4 import BeautifulSoup
import json


url = "https://www.mse.mk/mk"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# "Најтргувани"
table = soup.find('div', {'id': 'topSymbolValueTopSymbols'}).find('table')

headers = [th.text.strip() for th in table.find_all('th')]

data = {}
for row in table.find_all('tr')[1:]:  # Прескокнување на првиот ред
    cells = row.find_all('td')
    if cells:
        symbol = cells[0].text.strip()  # Шифра на акцијата
        data[symbol] = {
            headers[1]: cells[1].text.strip(),  # Просечна цена
            headers[2]: cells[2].text.strip(),  # % пром.
            headers[3]: cells[3].text.strip()   # Промет во БЕСТ
        }

print(data)



