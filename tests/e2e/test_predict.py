from owrestimator.app.back import predict_world_record


def test_predict_world_record():
    predictions = predict_world_record("Dead Cells", "Any% Warpless")
    assert predictions is not None
