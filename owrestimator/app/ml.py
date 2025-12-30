from pathlib import Path
from typing import Callable

from joblib import load

from owrestimator.app.speedrun_com_gateway import GameCategoryWorldRecord

PredictFunction = Callable[[GameCategoryWorldRecord], float]


def predict_tas_time_from_wr(category_world_record: GameCategoryWorldRecord) -> float:
    model = load(Path("bin/time_prediction.joblib"))
    return model.predict(category_world_record.to_dataframe())[0]
