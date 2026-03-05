import os
import pygame
import sys
from settings import *

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.init_fonts()

    def init_fonts(self):
        font_path = os.path.join(self.current_dir, 'fonts', 'Emulogic-font.ttf')
        
        if not os.path.exists(font_path):
            print(f"ERROR: Font file not found at {font_path}")
            self.font = pygame.font.SysFont('Arial', 75)
            self.button_font = pygame.font.SysFont('Arial', 40)
        else:
            self.font = pygame.font.Font(font_path, 75)
            self.button_font = pygame.font.Font(font_path, 40)

    def display(self):
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 200))

        back_btn_rect = pygame.Rect(0, 0, 370, 60)
        back_btn_rect.center = (WIDTH // 2, 400)
        back_text = self.button_font.render("MAIN MENU", True, BLACK)
        back_text_rect = back_text.get_rect(center=back_btn_rect.center)
        
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BLACK)
            
            self.screen.blit(game_over_text, game_over_rect)

            pygame.draw.rect(self.screen, YELLOW, back_btn_rect)
            self.screen.blit(back_text, back_text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_btn_rect.collidepoint(mouse_pos):
                        running = False
        
            pygame.display.update()