from owrestimator.app.ml import predict_tas_time_from_wr
from owrestimator.app.speedrun_com_gateway import GameCategoryWorldRecord


def test_predict_tas_time_from_wr() -> None:
    assert (
        predict_tas_time_from_wr(
            GameCategoryWorldRecord(
                105.967, 8, 101, "http://www.speedrun.com/deadcells/run/mrd451dz"
            )
        )
        == 135.5705950429265
    )
