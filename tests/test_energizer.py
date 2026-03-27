import pytest
import time

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

@pytest.mark.energizer
def test_energizer_deactivation_after_duration(energizer):
    energizer.activate()
    assert energizer.is_active() is True

    energizer.start_time = time.time() - 11
    energizer.update()
    assert energizer.is_active() is False

@pytest.mark.energizer
def test_energizer_is_about_to_expire(energizer):
    energizer.activate()
    energizer.start_time = time.time() - 6
    assert energizer.is_about_to_expire() is False

    energizer.start_time = time.time() - 8
    assert energizer.is_about_to_expire() is True
    