import datetime
from typing import Callable

import pandas as pd
import srcomapi
import srcomapi.datatypes as src_datatype
from attr import dataclass

src_api = srcomapi.SpeedrunCom()


@dataclass(frozen=True)
class GameCategoryWorldRecord:
    time: float
    age: int
    nb_of_runs: int
    weblink: str

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "time": self.time,
                "age": self.age,
                "nb_of_runs": self.nb_of_runs,
            },
            index=[0],
        )


GetGameCategoryWorldRecord = Callable[[str, str], GameCategoryWorldRecord]


def get_game_categories(game_name: str) -> list[str]:
    return [
        category.name
        for category in _get_src_game(game_name).categories
        if category.type != "per-level"
    ]


def get_game_category_world_record(
    game_name: str, category_name: str
) -> GameCategoryWorldRecord:
    src_game = _get_src_game(game_name)
    src_category = [
        category for category in src_game.categories if category.name == category_name
    ][0]

    category = src_datatype.Leaderboard(
        src_api,
        src_api.get(
            "leaderboards/{}/category/{}?embed=variables".format(
                src_game.id, src_category.id
            )
        ),
    )

    return GameCategoryWorldRecord(
        category.runs[0]["run"].times["primary_t"],
        datetime.datetime.now().year - src_game.released,
        len(category.runs),
        category.runs[0]["run"].weblink,
    )


def _get_src_game(game_name: str) -> src_datatype.Game:
    return src_api.search(srcomapi.datatypes.Game, {"name": game_name})[0]
