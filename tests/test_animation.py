import pytest


@pytest.mark.animation
def test_ghost_animation_timer_reset(ghost):
    ghost.anim_timer = 1.9
    ghost.anim_speed = 0.2

    ghost.update_animation()

    assert ghost.anim_timer == 0
    assert ghost.frame_index == 0


@pytest.mark.animation
def test_pacman_idle_animation(pacman):
    pacman.direction = (0, 0)
    pacman.update_animation()

    assert pacman.frame_index == 2


@pytest.mark.animation
def test_pacman_moving_animation_progression(pacman):
    pacman.direction = (1, 0)
    pacman.anim_timer = 1.0
    pacman.anim_speed = 1.0

    pacman.update_animation()

    assert pacman.anim_timer == 2.0
    assert pacman.frame_index == 2


@pytest.mark.animation
def test_pacman_animation_timer_reset(pacman):
    pacman.direction = (1, 0)
    pacman.anim_timer = 3.9
    pacman.anim_speed = 0.2

    pacman.update_animation()

    assert pacman.anim_timer == 0
    assert pacman.frame_index == 0
