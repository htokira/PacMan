import pytest

@pytest.mark.energizer
def test_energizer_activation(energizer):
    energizer.activate()
    assert energizer.is_active() == True
    assert energizer.ghosts_eaten == 0

@pytest.mark.energizer
def test_ghost_score_progression(energizer):
    assert energizer.get_next_ghost_score() == 200
    assert energizer.get_next_ghost_score() == 400
    assert energizer.get_next_ghost_score() == 800
    assert energizer.get_next_ghost_score() == 1600