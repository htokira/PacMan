import sys
import os
import pytest
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from map import Map
from ghost import Ghost

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()

@pytest.fixture
def create_map():
    def _create(level_data):
        return Map(screen=None, level_data=level_data, level_color=None, width=100, height=100)
    return _create
    
@pytest.fixture
def ghost():
    return Ghost("Blinky", "blinky.png", 100, 100, 34, (0, 0))
