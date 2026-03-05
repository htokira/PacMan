import os
import pygame
import sys
from settings import *

class WinScreen:
    def __init__(self, screen, is_cli=False):
        self.screen = screen
        self.is_cli = is_cli
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.init_fonts()

    def init_fonts(self):
        font_path = os.path.join(self.current_dir, 'fonts', 'Emulogic-font.ttf')
        if not os.path.exists(font_path):
            self.font = pygame.font.SysFont('Arial', 75)
            self.button_font = pygame.font.SysFont('Arial', 40)
        else:
            self.font = pygame.font.Font(font_path, 75)
            self.button_font = pygame.font.Font(font_path, 40)

    def display(self):
        win_text = self.font.render("YOU WIN!", True, GREEN) 
        win_rect = win_text.get_rect(center=(WIDTH // 2, 200))
        
        running = True
        while running:
            self.screen.fill(BLACK)
            self.screen.blit(win_text, win_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            
            pygame.display.update()