import pygame
import pytest
from map import Map

@pytest.fixture
def create_map():
    def _create(level_data):
        return Map(None, level_data, None, 100, 100)
    return _create

@pytest.mark.map
@pytest.mark.parametrize("level_data, test_x, test_y, expected", [
    ([[0]], 10, 10, True),
    ([[1]], 10, 10, True),
    ([[2]], 10, 10, True),
    ([[3]], 10, 10, False),
    ([[0]], -10, -10, False),
])
def test_can_move(create_map, level_data, test_x, test_y, expected):
    m = create_map(level_data)
    
    assert m.can_move(test_x, test_y) == expected