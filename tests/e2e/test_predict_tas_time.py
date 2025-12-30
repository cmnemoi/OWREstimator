from owrestimator.app.back import predict_tas_time


def test_predict_tas_time() -> None:
    predictions = predict_tas_time(game="Dead Cells", user_category="Any% Warpless")
    assert predictions is not None
