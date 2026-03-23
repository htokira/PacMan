from .base_screen import BaseEndScreen
from settings import RED


class GameOverScreen(BaseEndScreen):
    """Екран програшу, що наслідує базовий функціонал."""
    def display(self):
        super().display("GAME OVER", RED)
