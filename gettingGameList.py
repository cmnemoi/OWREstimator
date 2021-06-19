from bs4 import BeautifulSoup
import urllib.request
import csv

#getting a list of games
url_game_list = "http://tasvideos.org/Movies-RatingY.html"
page = urllib.request.urlopen(url_game_list)
soup = BeautifulSoup(page, 'html.parser')

spans = soup.find_all('span',attrs={'class':'thin'})
game_list = []
for span in spans:
    game_list.append(span.previous_element)

# Create csv and write rows to output file
with open('gamelist.csv','w') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(game_list)