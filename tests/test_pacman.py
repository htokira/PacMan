import pytest
import pygame
from unittest.mock import patch, MagicMock


@pytest.mark.pacman
def test_pacman_initial_pos(pacman):
    """Перевіряємо координати Пакмена (беремо з фікстури pacman)"""
    assert pacman.rect.x == 100
    assert pacman.rect.y == 100


@pytest.mark.pacman
def test_pacman_update_movement(pacman, create_map):
    """Перевіряємо реакцію Пакмена на натискання клавіш та зміну напрямку"""
    # 1. Створюємо пусту карту через фікстуру
    game_map = create_map([[0, 0, 0], [0, 0, 0]])

    # 2. Ставимо Пакмена в центр тайла
    pacman.rect.topleft = (32, 32)
    pacman.direction = (0, 0)

    # Мокаємо натискання клавіші "Вправо"
    with patch("pygame.key.get_pressed") as mock_keys:
        mock_return = MagicMock()
        mock_return.__getitem__.side_effect = lambda x: 1 if x == pygame.K_RIGHT else 0
        mock_keys.return_value = mock_return

        # 3. Викликаємо метод оновлення
        pacman.update(game_map)

        # Перевіряємо, що напрямок змінився на "вправо" (speed, 0)
        assert pacman.direction == (pacman.speed, 0)


@pytest.mark.pacman
def test_pacman_can_move_to_wall(pacman, create_map):
    game_map = create_map([[0, 3]])  # Пусто, Стіна
    pacman.rect.topleft = (0, 0)
    # Перевіряємо точку 40 (це точно друга клітинка, бо 40 > 32)
    assert pacman.can_move_to(40, 16, game_map) is False
