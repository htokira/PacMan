import pytest

@pytest.mark.ghost
def test_ghost_vulnerability_toggle(ghost):
    ghost.start_vulnerable()
    assert ghost.is_vulnerable == True
    
    ghost.stop_vulnerable()
    assert ghost.is_vulnerable == False

@pytest.mark.ghost
@pytest.mark.parametrize("initial_mode, is_vuln, expected_eaten, expected_killed, expected_mode", [
    ("CHASE", False, False, True, "CHASE"),
    ("CHASE", True, True, False, "RETURNING"),
    ("RETURNING", False, False, False, "RETURNING")
])
def test_handle_collision_states(ghost, initial_mode, is_vuln, expected_eaten, expected_killed, expected_mode):
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