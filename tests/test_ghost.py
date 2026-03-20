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