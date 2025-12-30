import datascrapper as ds
import pandas as pd
import urllib.error
import time


def collect_data(game):
    global game_list
    try:
        game_list = game_list.append(
            {
                **{**ds.get_fastest_TAS_time(game), **ds.get_category(game)},
                **ds.get_emulator(game),
            },
            ignore_index=True,
        )
        print(game + " infos collected")
    except AttributeError:
        game_list = game_list.append(
            {
                "game": game,
                "TAS_time(seconds)": pd.NA,
                "category": pd.NA,
                "emulator": pd.NA,
            },
            ignore_index=True,
        )


def formating_df():
    global game_list
    game_list.drop(game_list.head(743).index, inplace=True)
    game_list.reset_index(inplace=True)
    game_list.drop("index", axis=1, inplace=True)


game_list = pd.read_csv("gamelist.csv")
nb_games = len(game_list)


for game in game_list["game"]:
    try:
        collect_data(game)
    except urllib.error.HTTPError:
        time.sleep(60)
        collect_data(game)

formating_df()
game_list.to_csv("tas_dataset.csv")

print(game_list)
