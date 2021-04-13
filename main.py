import itertools
import json
import requests
from bs4 import BeautifulSoup
from helpers import get_mps_links

import pprint
pp = pprint.PrettyPrinter(indent=4)

base_url = 'https://parliament.gov.uz'
mps_list_url = '/uz/about/structure/deputy/'

page = requests.get(f'{base_url}{mps_list_url}')
soup = BeautifulSoup(page.content, 'html5lib')

alphabet = soup.select('.list-group-item ul li a')
char_links = [f'{base_url}{char["href"]}' for char in alphabet]

msp_links = []

for link in char_links:
    msp_links.append(get_mps_links(link))

msp_links = list(itertools.chain.from_iterable(msp_links))

msp = []

for mp_link in msp_links:
    mp_page = requests.get(f'{base_url}{mp_link}')
    soup = BeautifulSoup(mp_page.content, 'html5lib')
    mp_title = soup.select('.detal_title h3')[0]
    mp_details = soup.find('div', class_='deputats_info')
    mp_details_item = mp_details.select('p span')

    mp_adds = soup.find('div', class_='list-group-item')
    mp_adds_item = mp_adds.select('p span')

    mp_data = {
        'name': mp_title.string,
        'job': mp_details_item[0].string,
        'birth_date': mp_details_item[1].string,
        'birth_place': mp_details_item[2].string,
        'nationality': mp_details_item[3].string,
        'edu_level': mp_details_item[4].string,
        'edu_place': mp_details_item[5].string,
        'edu_major': mp_details_item[6].string,
        'acad_degree': mp_details_item[7].string,
        'acad_title': mp_details_item[8].string,
        'langs': mp_details_item[9].string,
        'extra_info': {
            'region': mp_adds_item[0].string,
            'constituency': mp_adds_item[1].string,
            'committee': mp_adds_item[2].string,
            'faction': mp_adds_item[3].string,
            'panel': mp_adds_item[4].string,
            'party': mp_adds_item[5].string,
            'candidacy': mp_adds_item[6].string,
            'awards': mp_adds_item[7].string,
        }
    }

    msp.append(mp_data)


with open('msp.json', 'w', encoding='utf-8') as f:
    json.dump(msp, f, ensure_ascii=False, indent=4)




