from bs4 import BeautifulSoup
import urllib.request
import csv

#initialize the game
game = 'Metroid'
#going to game search page
url_search_results = 'http://tasvideos.org/Search.html?key='+game
page = urllib.request.urlopen(url_search_results)
soup = BeautifulSoup(page, 'html.parser')

all_p = soup.find_all('p') #getting all results

url_movie = "http://tasvideos.org"+all_p[2].a['href'] #taking the first result


#going to the first result page
page = urllib.request.urlopen(url_movie)
soup = BeautifulSoup(page, 'html.parser')

tab = soup.find('div',attrs={'class' : 'tabbertab','title' : 'History of this entry'})

a_runs = tab.find_all('a')
url_last_run = "http://tasvideos.org"+a_runs[len(a_runs)-1]['href'] #getting the oldest run url

#going to the oldest TAS page
page = urllib.request.urlopen(url_last_run)
soup = BeautifulSoup(page, 'html.parser')

#getting emulator
td = soup.find('td',attrs={'class':'misc'})
emulator = td.a.contents[0].split(' ')[0]

#getting time
t = a_runs[len(a_runs)-1].contents[0].split(' ')
time = t[len(t)-1]

#convert it in seconds
from datetime import datetime
x = datetime.strptime(time,'%M:%S.%f')
time = x.minute*60+x.second+x.microsecond/1000000

#to do : exception if the time have a hour value