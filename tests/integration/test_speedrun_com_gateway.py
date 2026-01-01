from owrestimator.app.speedrun_com_gateway import (
    get_game_categories,
    get_game_category_world_record,
)


def test_get_game_categories():
    assert get_game_categories("Dead Cells") == [
        "Any% Warpless",
        "Any% Warps",
        "Fresh File",
        "0-5BC",
        "5BC",
    ]


def test_get_game_category_world_record():
    category_world_record = get_game_category_world_record(
        "Dead Cells", "Any% Warpless"
    )
    assert isinstance(category_world_record.time, float)
    assert isinstance(category_world_record.age, int)
    assert isinstance(category_world_record.nb_of_runs, int)
    assert category_world_record.weblink.startswith("http://www.speedrun.com/deadcells")
