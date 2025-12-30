import datetime
from dataclasses import dataclass

from owrestimator.app.ml import PredictFunction, predict_tas_time_from_wr
from owrestimator.app.speedrun_com_gateway import (
    GetGameCategoryWorldRecord,
    get_game_category_world_record,
)


@dataclass(frozen=True)
class TASPrediction:
    predicted_time: str
    WR_link: str
    WR_time: str


def predict_tas_time(
    game: str,
    user_category: str,
    get_game_category_world_record: GetGameCategoryWorldRecord = get_game_category_world_record,
    predict_tas_time_from_wr: PredictFunction = predict_tas_time_from_wr,
) -> TASPrediction:
    category_world_record = get_game_category_world_record(game, user_category)

    return TASPrediction(
        str(
            datetime.timedelta(seconds=predict_tas_time_from_wr(category_world_record))
        ),
        category_world_record.weblink,
        str(datetime.timedelta(seconds=category_world_record.time)),
    )
