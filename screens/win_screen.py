from .base_screen import BaseEndScreen
from settings import GREEN

class WinScreen(BaseEndScreen):
    """Екран перемоги, що наслідує базовий функціонал."""
    def display(self):
        super().display("YOU WIN!", GREEN)