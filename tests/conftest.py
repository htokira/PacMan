import sys
import os
import pytest
import pygame
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from map import Map
from ghost import Ghost
from energizer import Energizer
from pacman import Pacman


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    yield
    pygame.quit()


@pytest.fixture
def create_map():
    def _create(level_data):
        tile_size = 32
        # Розраховуємо ширину/висоту так, щоб тайл був рівно 32 пікселі
        width = len(level_data[0]) * tile_size
        height = len(level_data) * tile_size + 50
        m = Map(None, level_data, (0, 0, 255), width, height)
        m.w, m.h = tile_size, tile_size
        return m
    return _create


@pytest.fixture(autouse=True)
def mock_pygame_images():
    with patch("pygame.image.load") as mock_load:
        mock_load.return_value = pygame.Surface((32, 32))
        yield


@pytest.fixture
def pacman():
    return Pacman(100, 100)


@pytest.fixture
def ghost():
    # Додаємо відсутні аргументи (tile_size та scatter_targets)
    # 32 - це стандартний розмір тайла, [(0,0)] - список цілей для розсіювання
    return Ghost("Blinky", "blinky.png", 100, 100, 32, [(0, 0)])


@pytest.fixture
def energizer():
    return Energizer()
