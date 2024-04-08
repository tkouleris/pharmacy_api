from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here

    response = requests.get('https://fsa-efimeries.gr/')
    soup = BeautifulSoup(response.text, 'html.parser')

    select = soup.findChildren('select', {'id': 'Date'})

    children = select[0].findChildren("option", recursive=False)
    date = children[0].text.strip()

    tables = soup.findChildren('table')
    my_table = tables[0]
    rows = my_table.findChildren(['th', 'tr'])
    total_rows = []
    keys = [
        '-',
        '-',
        'perioxi',
        'farmakeio',
        'dieuthinsi',
        'tilefono',
        'orario',
        'katastasi'
    ]
    for row in rows:
        cells = row.findChildren('td')
        if len(cells) == 0:
            continue
        final_row = {
            'perioxi': '',
            'farmakeio': '',
            'dieuthinsi': '',
            'tilefono': '',
            'orario': '',
            'katastasi': ''
        }
        index = 0
        for cell in cells:
            if index in [0, 1]:
                index += 1
                continue
            final_row[keys[index]] = cell.text.strip()
            index += 1
        total_rows.append(final_row)

    pharmacies = []
    districts = []
    for farmakeio_row in total_rows:
        if farmakeio_row['perioxi'] not in districts:
            districts.append(farmakeio_row['perioxi'])
        pharmacies.append(farmakeio_row)

    return {'date': date, 'districts': districts, 'pharmacies': pharmacies}


if __name__ == '__main__':
    app.run()
