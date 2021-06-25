from os import times
from bs4 import BeautifulSoup
import urllib.request
import csv
import pandas as pd

def getting_page():
    url_game_list = "http://tasvideos.org/MoviePublishingHistory.html"
    page = urllib.request.urlopen(url_game_list)
    soup = BeautifulSoup(page, 'html.parser')

    return soup

def get_game_list(soup):

    brs = soup.find_all('br')
    game_list = []
    i=1
    for br in brs:
        try:
            string = br.previous_element.previous_element
            game=string.split('by')[0].split(' ',1)[1].split('"')[0].split('(')[0].rstrip()
            print(game)
            # print("Game n°"+str(i)+"/"+str(len(brs))+" infos collected")
            # i+=1
        except TypeError:
            print("Couldn't manage to collect game data ! (TypeError)")
            i += 1
            continue
        except IndexError:
            print("Couldn't manage to collect game data ! (IndexError)")
            i += 1
            continue
        try:
            category = string.split('"')[1]
            print(category)
        except IndexError:
            category = 'Any%'
            print(category)
        time = string.split(' ')[len(string.split(' '))-1]
        if time == '':
            continue
        print(time)
            # convert it in seconds
        from datetime import datetime
        try:
            x = datetime.strptime(time,'%H:%M:%S.%f')
        except ValueError:
            x = datetime.strptime(time,'%M:%S.%f')
        time = x.hour*3600+x.minute*60+x.second+x.microsecond/1000000
        game_list.append({'game':game,'category':category,'TAS_time(seconds)':time})

    return game_list

game_list = pd.DataFrame()
game_list = game_list.append(get_game_list(getting_page()))
game_list.to_csv('data/gamelist.csv')

# s = 'GBC Pokémon: Gold Version by CasualPokePlayer in 03:14.16'
# print(s.split(' ')[len(s.split(' '))-1])

# df = pd.DataFrame()

# l = []
# l.append({'game':'x','category':'p'})
# l.append({'game':'y','category':'z'})
# print(l)
# print(df.append(l))