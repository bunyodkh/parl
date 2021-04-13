import requests
from bs4 import BeautifulSoup


def get_mps_links(url):
    mps_urls = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')
    link_tags = soup.select('.fraction_session_element .col-md-10 h5 a')
    for link_tag in link_tags:
        mps_urls.append(link_tag['href'])
    return mps_urls
