import pandas as pd
import srcomapi, srcomapi.datatypes as dt

api = srcomapi.SpeedrunCom(); api.debug = 1
game_list = pd.read_csv('dataset.csv')

for i in range(len(game_list.index)):
      try:
        game = api.search(srcomapi.datatypes.Game, {"name": game_list.loc[i,'game']})[0]
      except IndexError:
        continue
      try:
        game_list.loc[i,'main_region'] = game.regions[0].name
      except IndexError:
        game_list.loc[i,'main_region'] = pd.NA
        game_list.loc[i,'nb_of_regions'] = pd.NA
        continue
      try:
        game_list.loc[i,'nb_of_regions'] = len(game.regions)
      except TypeError:
        continue

        

game_list.to_csv('dataset.csv')
