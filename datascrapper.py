from bs4 import BeautifulSoup
import urllib.request
import csv

game = 'Metroid'
url_search_results = 'http://tasvideos.org/Search.html?key='+game


page = urllib.request.urlopen(url_search_results)

soup = BeautifulSoup(page, 'html.parser')

all_p = soup.find_all('p')

url_movie = "http://tasvideos.org"+all_p[2].a['href']

page = urllib.request.urlopen(url_movie)
soup = BeautifulSoup(page, 'html.parser')

tab = soup.find('div',attrs={'class' : 'tabbertab','title' : 'History of this entry'})

a_runs = tab.find_all('a')


