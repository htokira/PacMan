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
        return Map(screen=None, level_data=level_data, level_color=None, width=100, height=100)
    return _create
    
@pytest.fixture
def ghost():
    return Ghost("Blinky", "blinky.png", 100, 100, 34, (0, 0))
#jcnfnjxyf dthcsz ntcnsd
@pytest.fixture(autouse=True)
def mock_pygame_images():
    """Автоматично замінює завантаження картинок на пусті поверхні"""
    with patch("pygame.image.load") as mock_load:
        # Створюємо пусту картинку 32x32 пікселі
        mock_load.return_value = pygame.Surface((32, 32))
        yield
@pytest.fixture
def energizer():
    return Energizer()

@pytest.fixture
def pacman():
    return Pacman(100, 100)
