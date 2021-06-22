from re import findall
from bs4 import BeautifulSoup
import urllib.request
import pandas
from pandas.core.algorithms import take_1d, take_2d_multi
from pandas.core.indexes.base import Index
import time

def getting_page(game):
    try:
        page = urllib.request.urlopen('http://tasvideos.org/Game/'+urlify(game))
    except UnicodeEncodeError:
        game = game.replace('é','')
        page = urllib.request.urlopen('http://tasvideos.org/Game/'+urlify(game))
    except urllib.error.HTTPError:
        print("Waiting for the site to accept our request...")
        time.sleep(20)
        page = urllib.request.urlopen('http://tasvideos.org/Game/'+urlify(game))

    soup = BeautifulSoup(page, 'html.parser')

    return soup

def urlify(s):

    import re

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a -
    s = re.sub(r"\s+", '-', s)

    return s


def get_emulator(game):

    soup = getting_page(game)
    
    results = []
    result = {}
    # getting emulator
    table = soup.find_all('table',attrs={'class':'item'})[len(soup.find_all('table',attrs={'class':'item'}))-1]
    td = table.find('td',attrs={'class':'misc'})
    result['game'] = game
    result['emulator'] = td.a.contents[0].split(' ')[0]
    # results.append(result)
    return result

def get_category(game):
    soup = getting_page(game)

    results = []
    result = {}
    spans = soup.find_all('span',attrs={'class':'thin'})
    for span in spans:
        result['game'] = game
        try:
            result['category'] = span.next_sibling.split('"')[1]
        except IndexError:
            result['category'] = 'Any%'
        # results.append(result)
    return result

def get_fastest_TAS_time(game):
    soup = getting_page(game)
    # getting time
    results = []
    result = {}
    spans = soup.find_all('span',attrs={'class':'thin'})
    quote = '"'
    for span in spans:
        result['game'] = game
        if quote in span.next_sibling:
            if 'in' in span.next_sibling.split('"')[1]:
                time = span.next_sibling.split('in')[2].split('by')[0].split(' ')[1]
            else:
                time = span.next_sibling.split('in')[1].split('by')[0].split(' ')[1]
        else:
            time = span.next_sibling.split('in')[1].split('by')[0].split(' ')[1]
        # convert it in seconds
        from datetime import datetime
        try:
            x = datetime.strptime(time,'%H:%M:%S.%f')
        except ValueError:
            x = datetime.strptime(time,'%M:%S.%f')
        time = x.hour*3600+x.minute*60+x.second+x.microsecond/1000000
        result['TAS_time(seconds)'] = time   
        # results.append(result)
    return result
