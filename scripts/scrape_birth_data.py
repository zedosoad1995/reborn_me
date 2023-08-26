from bs4 import BeautifulSoup
import csv
import re
import requests

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_number_of_births'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})

data = []

for row in table.findAll('tr')[1:]:
    cells = row.findAll('td')
    if len(cells) > 1:
        country = cells[1].get_text().strip()
        rate = int(re.match(r'\d+', cells[-1].get_text().strip().replace(',', '')).group())
        data.append((country, rate))

with open('data/country_birth_rates.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Country", "Num of Births"])
    csv_writer.writerows(data)
