import srcomapi, srcomapi.datatypes as dt
import pandas as pd
api = srcomapi.SpeedrunCom(); api.debug = 1

game_list = pd.read_csv('gamelist.csv')

game_list.rename(columns={'NES Mega Man 2':'Game'},inplace=True)
game_list.loc[742] = 'Mega Man 2'
game_list.drop_duplicates()
print(len(game_list))
