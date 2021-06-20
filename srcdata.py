from pandas._libs.missing import NA
import srcomapi, srcomapi.datatypes as dt
import pandas as pd
import numpy as np

api = srcomapi.SpeedrunCom(); api.debug = 1

game_list = pd.read_csv('gamelist.csv')

game_list.rename(columns={'NES Mega Man 2':'Game'},inplace=True)
game_list.loc[len(game_list)-1] = 'NES Mega Man 2'
game_list.drop_duplicates()

# removing the platform from the gane name
for i in range(len(game_list)):
    game_list.loc[i] = game_list.loc[i].values[0].split(' ', 1)[1]

test_df = game_list
nb_games = len(test_df)

# test_df = pd.DataFrame(['Castlevania: Aria of Sorrow','Pokémon: Yellow'],columns=['Game'])


lb_per_game = []



# getting the game for each name
for i in range(nb_games):
    try:
      test_df.loc[i,'SRC_game'] = api.search(srcomapi.datatypes.Game, {"name": test_df.loc[i]['Game']})[0]
    except IndexError:
      pass
# print(test_df.tail())
test_df.dropna(inplace=True)
nb_games = len(test_df)
test_df.reset_index(inplace=True,drop=True)
# print(test_df.tail())


# print(nb_games)
# collecting leaderboards for each game
for i in range(nb_games):
    lb = {}
    game = test_df.loc[i,'SRC_game']
    try:
      for category in game.categories:
        if not category.name in lb:
          lb[category.name] = {}
        if category.miscellaneous:
          pass
        elif category.type == 'per-level':
          for level in game.levels:
            try:
              lb[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}/{}?embed=variables".format(test_df.loc[i,'SRC_game'].id, category.id,level.id)))
            except srcomapi.exceptions.APIRequestException:
              pass
        else:
          try:
            lb[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(test_df.loc[i,'SRC_game'].id, category.id)))
          except KeyError:
            pass
          except srcomapi.exceptions.APIRequestException:
            pass
    except AttributeError:
      continue
    lb_per_game.append(lb)

# print(nb_games)
# print(len(lb_per_game))
a = np.array([])

# collecting WR times with its category and features : name, released year, nb of runs

for i in range(len(lb_per_game)):
  for j in lb_per_game[i].keys():
    try:
      game_name = lb_per_game[i][j].game.names['international']
      category_name = j
      try:
        WR_time = lb_per_game[i][j].runs[0]["run"].times['realtime_t']
      except IndexError:
        pass
      released_year = lb_per_game[i][j].game.released
      a=np.append(a, [ game_name, category_name, WR_time, released_year, len(lb_per_game[i][j].runs)  ] )
    except AttributeError:
      pass  

test_df = pd.DataFrame(a.reshape(int(len(a)/5),5),columns=['game','category','time(seconds)','released_year','nb_of_runs'])

test_df.to_csv('dataset.csv')


features = ['platforms','genres','engines','developers','publishers']
for feature in features:
  for i in range(len(test_df.index)):
    print(i)
    print(test_df.loc[i,'game'])
    game = api.search(srcomapi.datatypes.Game, {"name": test_df.loc[i,'game']})[0]
    try:
      test_df.loc[i,feature] = game.__getattr__(feature)[0].name
    except IndexError:
      test_df.loc[i,feature] = NA

print(test_df)

test_df.to_csv('dataset.csv')




# features = {'platforms': [], 'regions':[],'genres':[],'developers':[],'publishers':[]}
# for feature in features:   
#   print(lb_per_game[0]['Soma Any%'].game.__getattr__(feature))

# # print(lb_per_game)
# feature = ['platforms','genres']
# for feature in features:
#   print(lb_per_game[0]['Soma Any%'].game.__getattr__(f))
# test_df["leaderboards"] = lb_per_game
# print(df_lb) 
# test_df = pd.concat([test_df,df_lb])
# print(test_df)
# print(test_df.columns)
# g_lb = {}
# for category in srcgames[0].categories:
  

# print(lb_per_game[0]['Soma Any% No 0HP'].game.genres)
# print(g_lb['Soma Any%'].lb[0]['run'].times['primary_t'])

# dictOfStuff = {} ##Make a Dictionary
# features = {'platforms': [], 'regions':[],'genres':[],'developers':[],'publishers':[]}

# x = 'platforms' ##OR it can equal the input of something, up to you.

# dictOfStuff[x] = 4 ##Get the dict spot that has the same key ("name") as what X is equal to. In this case "Buffalo". and set it to 4. Or you can set it to  what ever you like

# print(type(x)) ##print out the value of the spot in the dict that same key ("name") as the dictionary.

# platform = lb_per_game[0]['Soma Any%'].game.__getattr__('platforms')[0]
# print(platform)

# for i in range(2):
#   game = lb_per_game[0]['Soma Any%'].game
#   platform = game.__getattr__('genres')[0]
#   print(platform)
    
#     features = {'platforms': [], 'regions':[],'genres':[],'developers':[],'publishers':[]}
#     for feature in features:
#       for k in range(len(lb_per_game[i][j].game.data[feature])):
#         test0 = lb_per_game[i][j].game
#         test1 = lb_per_game[i][j].game.__getattr__(feature)
#         test2 = test1[k]
#         test3 = test1[k].data
#         test4 = test1[k].data['name']

#         features[feature].append(test4)
#           print(lb_per_game[0]['Soma Any%'].game.__getattr__(feature))
#     # a=np.append(a,[features[feature]])
