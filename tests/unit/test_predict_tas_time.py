import datetime

from owrestimator.app.back import TASPrediction, predict_tas_time
from owrestimator.app.speedrun_com_gateway import GameCategoryWorldRecord


def fake_get_game_category_world_record(
    game: str, category: str
) -> GameCategoryWorldRecord:
    return GameCategoryWorldRecord(
        105.967, 8, 101, "http://www.speedrun.com/deadcells/run/mrd451dz"
    )


def fake_predict_tas_time_from_wr(
    category_world_record: GameCategoryWorldRecord,
) -> float:
    return 100


def test_predict_tas_time() -> None:
    assert predict_tas_time(
        "Dead Cells",
        "Any% Warpless",
        fake_get_game_category_world_record,
        fake_predict_tas_time_from_wr,
    ) == TASPrediction(
        str(datetime.timedelta(seconds=100)),
        "http://www.speedrun.com/deadcells/run/mrd451dz",
        str(datetime.timedelta(seconds=105.967)),
    )
