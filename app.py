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

    response = requests.get('https://fsa-efimeries.gr/Home/FilteredHomeResults')
    soup = BeautifulSoup(response.text, 'html.parser')

    cards = soup.select(".card-frame")

    # for card in cards:
    #     title = card.select_one(".card-title h6").get_text(strip=True)
    #     print(title)
    #     exit()

    #
    # children = select[0].findChildren("option", recursive=False)
    # date = children[0].text.strip()
    #
    # tables = soup.findChildren('table')
    # my_table = tables[0]
    # rows = my_table.findChildren(['th', 'tr'])
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
    for card in cards:
        title = card.select_one(".card-title h6").get_text(strip=True)
        subtitle = card.select_one(".card-subtitle").get_text(strip=True)
        pharmacist = card.select_one(".card-text span:nth-of-type(1)").get_text(strip=True)
        hours = card.select_one(".card-text span:nth-of-type(2)").get_text(strip=True)
        phone = card.select_one(".card-text h6").get_text(strip=True)

        status_img = card.select_one("img")
        status_src = status_img["src"]

        if "anoixto" in status_src:
            status = "Ανοιχτό"
        elif "kleisto" in status_src:
            status = "Κλειστό"
        else:
            status = "Άγνωστο"

        final_row = {
            'perioxi': subtitle,
            'farmakeio': pharmacist,
            'dieuthinsi': title,
            'tilefono': phone,
            'orario': hours,
            'katastasi': status
        }
        #     index = 0
        #     for cell in cells:
        #         if index in [0, 1]:
        #             index += 1
        #             continue
        #         final_row[keys[index]] = cell.text.strip()
        #         index += 1
        total_rows.append(final_row)
    #
    pharmacies = []
    districts = []
    for farmakeio_row in total_rows:
        if farmakeio_row['perioxi'] not in districts:
            districts.append(farmakeio_row['perioxi'])
        pharmacies.append(farmakeio_row)
    return {'date': date, 'districts': districts, 'pharmacies': pharmacies}
    # response = requests.get('https://fsa-efimeries.gr/')
    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # select = soup.findChildren('select', {'id': 'Date'})
    #
    # children = select[0].findChildren("option", recursive=False)
    # date = children[0].text.strip()
    #
    # tables = soup.findChildren('table')
    # my_table = tables[0]
    # rows = my_table.findChildren(['th', 'tr'])
    # total_rows = []
    # keys = [
    #     '-',
    #     '-',
    #     'perioxi',
    #     'farmakeio',
    #     'dieuthinsi',
    #     'tilefono',
    #     'orario',
    #     'katastasi'
    # ]
    # for row in rows:
    #     cells = row.findChildren('td')
    #     if len(cells) == 0:
    #         continue
    #     final_row = {
    #         'perioxi': '',
    #         'farmakeio': '',
    #         'dieuthinsi': '',
    #         'tilefono': '',
    #         'orario': '',
    #         'katastasi': ''
    #     }
    #     index = 0
    #     for cell in cells:
    #         if index in [0, 1]:
    #             index += 1
    #             continue
    #         final_row[keys[index]] = cell.text.strip()
    #         index += 1
    #     total_rows.append(final_row)
    #
    # pharmacies = []
    # districts = []
    # for farmakeio_row in total_rows:
    #     if farmakeio_row['perioxi'] not in districts:
    #         districts.append(farmakeio_row['perioxi'])
    #     pharmacies.append(farmakeio_row)
    #
    # return {'date': date, 'districts': districts, 'pharmacies': pharmacies}


if __name__ == '__main__':
    app.run()
