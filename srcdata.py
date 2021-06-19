from posixpath import split
import srcomapi, srcomapi.datatypes as dt
import pandas as pd
import numpy as np
api = srcomapi.SpeedrunCom(); api.debug = 1

game_list = pd.read_csv('gamelist.csv')

game_list.rename(columns={'NES Mega Man 2':'Game'},inplace=True)
game_list.loc[742] = 'NES Mega Man 2'
game_list.drop_duplicates()

#removing the platform from the gane name
for i in range(len(game_list)):
    game_list.loc[i] = game_list.loc[i].values[0].split(' ', 1)[1]

test_df = game_list.head(2)
nb_games = len(test_df)

lb_per_game = []

for i in range(nb_games):
    try: 
      test_df.loc[i,'SRC_game'] = api.search(srcomapi.datatypes.Game, {"name": test_df.loc[i]['Game']})[0]
    except IndexError:
      pass

for i in range(nb_games):
    lb = {}
    for category in test_df.loc[i,'SRC_game'].categories:
      if not category.name in lb:
        lb[category.name] = {}
      if category.type == 'per-level':
        pass
      # if category.miscellaneous:
      #   pass
      else:
        lb[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(test_df.loc[i,'SRC_game'].id, category.id)))
    lb_per_game.append(lb)

a = np.array([])


for i in range(nb_games):
  for j in lb_per_game[i].keys():
    try:
      a=np.append(a, [ lb_per_game[i][j].game.names['international'], j, lb_per_game[i][j] ] )
    except AttributeError:
      pass




# print(lb_per_game)
# print(lb_per_game[0]['Soma Any%'].game.names['international'])

# test_df["leaderboards"] = lb_per_game
print(pd.DataFrame(a.reshape(13,3)))
# print(df_lb) 
# test_df = pd.concat([test_df,df_lb])
# print(test_df)
# print(test_df.columns)
# g_lb = {}
# for category in srcgames[0].categories:
#   


# print(g_lb['Soma Any%'].lb[0]['run'].times['primary_t'])

