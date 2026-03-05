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

        # Кнопка
        back_btn_rect = pygame.Rect(0, 0, 370, 60)
        back_btn_rect.center = (WIDTH // 2, 400)
        
        button_label = "EXIT" if self.is_cli else "MAIN MENU"
        back_text = self.button_font.render(button_label, True, BLACK)
        back_text_rect = back_text.get_rect(center=back_btn_rect.center)
        
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BLACK)
            self.screen.blit(win_text, win_rect)

            pygame.draw.rect(self.screen, YELLOW, back_btn_rect)
            self.screen.blit(back_text, back_text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_btn_rect.collidepoint(mouse_pos):
                        if self.is_cli:
                            pygame.quit(); sys.exit()
                        else:
                            running = False
            
            pygame.display.update()