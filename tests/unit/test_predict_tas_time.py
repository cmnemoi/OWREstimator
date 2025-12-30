import datetime

from owrestimator.app.back import TASPrediction, predict_tas_time
from owrestimator.app.speedrun_com_gateway import GameCategoryWorldRecord


def test_predict_tas_time() -> None:
    assert predict_tas_time(
        "Dead Cells",
        "Any% Warpless",
        lambda game, category: GameCategoryWorldRecord(
            105.967, 8, 101, "http://www.speedrun.com/deadcells/run/mrd451dz"
        ),
        lambda _: 100,
    ) == TASPrediction(
        str(datetime.timedelta(seconds=100)),
        "http://www.speedrun.com/deadcells/run/mrd451dz",
        str(datetime.timedelta(seconds=105.967)),
    )
