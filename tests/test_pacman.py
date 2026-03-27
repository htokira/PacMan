import pytest
import pygame
from unittest.mock import patch
from unittest.mock import MagicMock


# Ця штука автоматично вимикає завантаження картинок для всіх тестів нижче
@pytest.fixture(autouse=True)
def mock_pygame_images():
    with patch("pygame.image.load") as mock_load:
        mock_load.return_value = pygame.Surface((34, 34))
        yield


# ТЕСТИ (мають починатися з test_)


def test_pacman_initial_pos(pacman):
    """Перевіряємо координати Пакмена"""
    assert pacman.rect.x == 100
    assert pacman.rect.y == 100


def test_ghost_initial_name(ghost):
    """Перевіряємо ім'я привида"""
    assert ghost.name == "Blinky"


def test_map_wall_collision(create_map):
    """Перевіряємо, чи бачить карта стіни (код 3)"""
    level_data = [[3, 3], [3, 3]]
    test_map = create_map(level_data)
    # Перевіряємо першу клітинку
    assert test_map.level[0][0] == 3

@pytest.mark.pacman
def test_pacman_update_movement(pacman, create_map):
    # 1. Створюємо карту 3х2 (пусту)
    game_map = create_map([[0, 0, 0], [0, 0, 0]])
    game_map.w, game_map.h = 32, 32
    game_map.width = 96

    # 2. СТАВИМО ПАКМЕНА В ЦЕНТР ТАЙЛА (наприклад, 32, 32)
    # Це критично для методу update!
    pacman.rect.topleft = (32, 32)
    pacman.direction = (0, 0) # зупиняємо його спочатку
    
    with patch("pygame.key.get_pressed") as mock_keys:
        mock_return = MagicMock()
        mock_return.__getitem__.side_effect = lambda x: 1 if x == pygame.K_RIGHT else 0
        mock_keys.return_value = mock_return
        
        # 3. Викликаємо update
        pacman.update(game_map)
        
        # Тепер він має відчути "магніт" і почати рух вправо
        assert pacman.direction == (pacman.speed, 0)
@pytest.mark.pacman
def test_pacman_can_move_to_wall(pacman, create_map):
    # Створюємо карту 2х2, де (1,0) - це стіна (код 3)
    level_data = [[0, 3], [0, 0]]
    game_map = create_map(level_data)
    game_map.width = 100 # задаємо розміри для телепортації
    
    pacman.direction = (pacman.speed, 0) # Пакмен хоче йти вправо
    # Перевіряємо, чи може він туди стати
    assert pacman.can_move_to(pacman.rect.x, pacman.rect.y, game_map) is False
