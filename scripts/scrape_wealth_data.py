from bs4 import BeautifulSoup
import csv
import re
import requests

url = 'https://en.wikipedia.org/wiki/Distribution_of_wealth'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})

data = []

for row in table.findAll('tr')[1:]:
    cells = row.findAll('td')
    lst = []
    if len(cells) > 1:
        lst.append(cells[0].get_text().strip())
        for i in range(2, 8):
            lst.append(float(cells[i].get_text().strip().replace(',', '')))
        data.append(tuple(lst))

with open('data/country_wealth.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Country', 'mean', 'median',
                        '<10k', '10-100k', '100k-1M', '1M+'])
    csv_writer.writerows(data)
