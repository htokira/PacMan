import pytest

from unittest.mock import MagicMock
import time


@pytest.mark.ghost
def test_ghost_full_lifecycle_update(ghost, create_map):
    # 1. Підготовка оточення
    game_map = create_map([[0] * 20 for _ in range(20)])  # Пуста карта
    mock_player = MagicMock()
    mock_player.rect.center = (100, 100)
    ghost.tile_size = 32

    # 2. ТЕСТ РЕЖИМУ WAITING (Перевірка затримки)
    ghost.mode = "WAITING"
    ghost.release_delay = 10
    ghost.start_time = time.time()  # щойно почав чекати

    ghost.update(mock_player, game_map, (0, 0))
    assert ghost.mode == "WAITING"  # має все ще чекати

    # 3. ТЕСТ ПЕРЕХОДУ В EXITING
    ghost.start_time = time.time() - 11  # "відмотуємо" час назад
    ghost.update(mock_player, game_map, (0, 0))
    assert ghost.mode == "EXITING"

    # 4. ТЕСТ ЛОГІКИ EXITING (Рух до брами)
    # Ставимо його нижче лінії брами (gate_y = 8 * 32 = 256)
    ghost.rect.y = 300
    ghost.rect.centerx = 10 * 32 + 16  # вирівняли по центру

    ghost.update(mock_player, game_map, (0, 0))
    assert ghost.rect.y < 300  # має рухатися вгору

    # 5. ТЕСТ ПЕРЕХОДУ В CHASE (Вихід на волю)
    ghost.rect.y = 8 * 32  # Досяг брами
    ghost.update(mock_player, game_map, (0, 0))
    # Перевіряємо, що режим змінився. Напрямок може бути різним залежно від Пакмена,
    # тому просто перевіримо, що він не нульовий.
    assert ghost.mode == "CHASE"
    assert ghost.direction[1] != 0  # він кудись рухається по вертикалі


@pytest.mark.ghost
def test_ghost_targets_player_optimally(ghost):
    # Створюємо мок гравця з РЕАЛЬНИМИ числами в rect
    mock_player = MagicMock()
    mock_player.rect.centerx = 128
    mock_player.rect.centery = 32

    ghost.rect.topleft = (32, 32)
    valid_dirs = [(2, 0), (0, 2)]  # Вправо або Вниз

    # Тепер calculate_distance отримає числа і порівняння спрацює
    best_dir = ghost.find_closest_direction(valid_dirs, mock_player)
    assert best_dir == (2, 0)


@pytest.mark.ghost
def test_ghost_vulnerability_toggle(ghost):
    ghost.start_vulnerable()
    assert ghost.is_vulnerable is True

    ghost.stop_vulnerable()
    assert ghost.is_vulnerable is False


@pytest.mark.ghost
@pytest.mark.parametrize(
    "initial_mode, is_vuln, expected_eaten, expected_killed, expected_mode",
    [
        ("CHASE", False, False, True, "CHASE"),
        ("CHASE", True, True, False, "RETURNING"),
        ("RETURNING", False, False, False, "RETURNING"),
    ],
)
def test_handle_collision_states(
    ghost, initial_mode, is_vuln, expected_eaten, expected_killed, expected_mode
):
    ghost.mode = initial_mode
    ghost.is_vulnerable = is_vuln

    eaten, killed = ghost.handle_player_collision()

    assert eaten == expected_eaten
    assert killed == expected_killed
    assert ghost.mode == expected_mode


@pytest.mark.ghost
def test_ghost_reverse_direction_on_vulnerability(ghost):
    ghost.mode = "CHASE"
    ghost.direction = (2, 0)
    ghost.start_vulnerable()
    assert ghost.is_vulnerable is True
    assert ghost.direction == (-2, 0)


@pytest.mark.ghost
def test_ghost_reset_to_returning_mode(ghost):
    ghost.mode = "CHASE"
    ghost.is_vulnerable = True

    ghost.reset(instant=False)

    assert ghost.mode == "RETURNING"
    assert ghost.is_vulnerable is False


@pytest.mark.ghost
def test_ghost_fly_home_movement(ghost):
    ghost.mode = "RETURNING"
    ghost.rect.center = (300, 300)
    initial_x, initial_y = ghost.rect.center
    ghost.fly_home()
    assert ghost.rect.centerx < initial_x
    assert ghost.rect.centery < initial_y


@pytest.mark.ghost
def test_ghost_fly_home_arrival(ghost):
    ghost.mode = "RETURNING"
    spawn_x, spawn_y = ghost.spawn_pos
    ghost.rect.center = (spawn_x + 1, spawn_y + 1)

    ghost.fly_home()
    assert ghost.rect.center == ghost.spawn_pos
    assert ghost.mode == "WAITING"
    assert ghost.is_vulnerable is False
