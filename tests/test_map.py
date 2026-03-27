import pytest


@pytest.mark.map
@pytest.mark.parametrize("level_data, test_x, test_y, expected", [
    ([[0]], 10, 10, True),
    ([[1]], 10, 10, True),
    ([[2]], 10, 10, True),
    ([[3]], 10, 10, False),
    ([[0]], -10, -10, False)])
def test_can_move(create_map, level_data, test_x, test_y, expected):
    m = create_map(level_data)

    assert m.can_move(test_x, test_y) == expected


@pytest.mark.map
@pytest.mark.parametrize("cell_value, expected_score, expected_energizer", [
    (1, 1, False),
    (2, 50, True),
    (0, 0, False)])
def test_collisions(create_map, cell_value, expected_score, expected_energizer):
    m = create_map([[cell_value]])

    score, energizer = m.collision_with_objects(10, 10)

    assert score == expected_score
    assert energizer == expected_energizer
    assert m.level[0][0] == 0


@pytest.mark.map
@pytest.mark.parametrize("level_data, expected_clear", [
    ([[0, 0], [0, 0]], True),
    ([[3, 4], [5, 6]], True),
    ([[1, 0], [0, 0]], False),
    ([[0, 2], [0, 0]], False)])
def test_is_clear(create_map, level_data, expected_clear):
    m = create_map(level_data)

    assert m.is_clear() == expected_clear
