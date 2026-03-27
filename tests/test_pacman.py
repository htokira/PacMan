import pytest
import pygame
from unittest.mock import patch, MagicMock

# ТЕСТИ ПАКМЕНА
#ocnfnjxyf dthcsz ntcnsd 
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
    """Перевіряємо, що Пакмен бачить стіну і не може туди йти"""
    # Створюємо карту: (0,0) - пусто, (0,1) - стіна (код 3)
    level_data = [[0, 3], [0, 0]]
    game_map = create_map(level_data)
    
    pacman.rect.topleft = (0, 0)
    pacman.direction = (pacman.speed, 0) # Хочемо йти вправо, де стіна
    
    # Перевіряємо метод перевірки можливості ходу
    # rect.x + speed — це спроба стати на координату стіни
    assert pacman.can_move_to(pacman.rect.x + pacman.speed, pacman.rect.y, game_map) is False