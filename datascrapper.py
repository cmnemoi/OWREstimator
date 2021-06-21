from bs4 import BeautifulSoup
import urllib.request


#initialize the game
game = 'celeste'

def get_random_movie_url(game):
    #going to game search page
    url_search_results = 'http://tasvideos.org/Search.html?key='+game
    page = urllib.request.urlopen(url_search_results)
    soup = BeautifulSoup(page, 'html.parser')
    all_p = soup.find_all('p') #getting all results

    return "http://tasvideos.org"+all_p[2].a['href'] #taking the first result

def get_fastest_movie_url(url_movie):
    page = urllib.request.urlopen(url_movie)
    soup = BeautifulSoup(page, 'html.parser')

    div = soup.find('div',attrs={'class' : 'tabbertab','title' : 'History of this entry'})

    a_runs = div.find_all('a')
    for i in range(len(a_runs)):
        url = "http://tasvideos.org"+a_runs[i]['href'] #getting the fastest run url
        if '.html' in url:
            break
    return url


def get_emulator(url):
    #going to the fastest TAS page
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    #getting emulator
    td = soup.find('td',attrs={'class':'misc'})
    return td.a.contents[0].split(' ')[0]

def get_fastest_TAS_time(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    #getting time
    div = soup.find('div',attrs={'class' : 'tabbertab','title' : 'History of this entry'})
    a_runs = div.find_all('a')
    index = 0
    for index in range(len(a_runs)):
        url = "http://tasvideos.org"+a_runs[index]['href'] #getting the fastest run url
        if '.html' in url:
            break
    time = a_runs[index].next_element.split(' ')[len(a_runs[index].next_element.split(' '))-1]

    #convert it in seconds
    from datetime import datetime
    try:
        x = datetime.strptime(time,'%H:%M:%S.%f')
    except ValueError:
        x = datetime.strptime(time,'%M:%S.%f')
    time = x.hour*3600+x.minute*60+x.second+x.microsecond/1000000
    return time

url_movie = get_random_movie_url(game)
fastest_movie_url = get_fastest_movie_url(url_movie)
emulator = get_emulator(fastest_movie_url)
time = get_fastest_TAS_time(fastest_movie_url)

