import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from map import Map


@pytest.fixture
def create_map():
    def _create(level_data):
        return Map(screen=None, level_data=level_data, level_color=None, width=100, height=100)
    return _create
