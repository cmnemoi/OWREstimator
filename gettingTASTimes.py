import datascrapper as ds
import pandas as pd

game_list = pd.read_csv('gamelist.csv')

i=0
nb_games = len(game_list)
for game in game_list['game']:
    i +=1
    game_list = game_list.append({ **{**ds.get_fastest_TAS_time(game),**ds.get_category(game)}, **ds.get_emulator(game) },ignore_index=True)
    print(game + ' infos collected')
    print(str(i)+"/"+str(nb_games) + " completed")



game_list.drop(game_list.head(743).index, inplace=True)
game_list.reset_index(inplace=True)
game_list.drop('index',axis=1,inplace=True)
game_list.to_csv('tas_dataset.csv')
print(game_list)

# d = {'game':'NES Mega Man 2'}
# e= {'category':'any%'}
#game_list = game_list.append(d,ignore_index=True)
# game_list = game_list.append({**d,**e},ignore_index=True)
# print(game_list)