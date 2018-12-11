import re
import urllib.request
from bs4 import BeautifulSoup
import dryscrape

packtpub_url = "https://www.packtpub.com"
freelearning_url = "https://www.packtpub.com/packt/offers/free-learning"


def get_book_title():
    c = urllib.request.urlopen(freelearning_url).read()
    soup = BeautifulSoup(c, 'lxml')

    title= soup.find('div', {'id':'title-bar-title'})
    title = title.find('h1')
    return title.text

def get_book_time():
    session = dryscrape.Session()
    session.visit(freelearning_url)
    response = session.body()

    soup = BeautifulSoup(response, 'lxml')
    tps_restant = soup.find('span', {'class':'packt-js-countdown'})

    return tps_restant.text