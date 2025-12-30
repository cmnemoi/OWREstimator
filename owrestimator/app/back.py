import datetime
from pathlib import Path

import pandas as pd
import srcomapi
import srcomapi.datatypes as dt
from joblib import load

api = srcomapi.SpeedrunCom()


def request_categories(name):
    src_game = api.search(srcomapi.datatypes.Game, {"name": name})[0]
    leaderboards = {}
    for category in src_game.categories:
        if category.type == "per-level":
            pass
        else:
            leaderboards[category.name] = dt.Leaderboard(
                api,
                data=api.get(
                    "leaderboards/{}/category/{}?embed=variables".format(
                        src_game.id, category.id
                    )
                ),
            )

    categories_names = []
    for lb in leaderboards:
        categories_names.append(lb)

    return categories_names


def predict_world_record(game, user_category):
    result = {}
    src_game = api.search(srcomapi.datatypes.Game, {"name": game})[0]

    leaderboards = {}
    for category in src_game.categories:
        if category.type == "per-level":
            pass
        else:
            leaderboards[category.name] = dt.Leaderboard(
                api,
                data=api.get(
                    "leaderboards/{}/category/{}?embed=variables".format(
                        src_game.id, category.id
                    )
                ),
            )

    pipeline = load(Path("bin/time_prediction.joblib"))
    nb_of_runs = len(leaderboards[user_category].runs)
    age = datetime.datetime.now().year - src_game.released
    WR_time = leaderboards[user_category].runs[0]["run"].times["primary_t"]

    df = pd.DataFrame(
        {
            "time": WR_time,
            "age": age,
            "nb_of_runs": nb_of_runs,
        },
        index=[0],
    )

    predicted_time = str(datetime.timedelta(seconds=pipeline.predict(df)[0]))
    WR_link = leaderboards[user_category].runs[0]["run"].weblink
    WR_time = str(
        datetime.timedelta(
            seconds=leaderboards[user_category].runs[0]["run"].times["primary_t"]
        )
    )

    result["predicted_time"] = predicted_time
    result["WR_link"] = WR_link
    result["WR_time"] = WR_time

    return result
