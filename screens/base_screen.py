import os
import pygame
import sys
from settings import *

class BaseEndScreen:
    """
    Базовий клас для фінальних екранів гри (Перемога/Програш).
    """
    def __init__(self, screen, score, is_cli=False):
        self.screen = screen
        self.score = score
        self.is_cli = is_cli
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_dir = os.path.join(os.path.dirname(self.current_dir), 'fonts')
        self.init_fonts()

    def init_fonts(self):
        font_path = os.path.join(self.font_dir, 'Emulogic-font.ttf')
        
        if not os.path.exists(font_path):
            self.font = pygame.font.SysFont('Arial', 75)
            self.score_font = pygame.font.SysFont('Arial', 30)
            self.button_font = pygame.font.SysFont('Arial', 40)
        else:
            self.font = pygame.font.Font(font_path, 75)
            self.score_font = pygame.font.Font(font_path, 30)
            self.button_font = pygame.font.Font(font_path, 40)

    def _render_common_elements(self, title_text, title_color):
        """Внутрішній метод для підготовки спільних елементів інтерфейсу."""
        title_surf = self.font.render(title_text, True, title_color)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 200))

        score_surface = self.score_font.render(f"FINAL SCORE: {self.score}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 300))

        back_btn_rect = pygame.Rect(0, 0, 370, 60)
        back_btn_rect.center = (WIDTH // 2, 400)
        
        button_label = "EXIT" if self.is_cli else "MAIN MENU"
        back_text = self.button_font.render(button_label, True, BLACK)
        back_text_rect = back_text.get_rect(center=back_btn_rect.center)
        
        return title_surf, title_rect, score_surface, score_rect, back_btn_rect, back_text, back_text_rect

    def display(self, title_text, title_color):
        """Загальний цикл відображення."""
        (title_surf, title_rect, score_surface, score_rect, 
         back_btn_rect, back_text, back_text_rect) = self._render_common_elements(title_text, title_color)

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BLACK)
            
            self.screen.blit(title_surf, title_rect)
            self.screen.blit(score_surface, score_rect)
            pygame.draw.rect(self.screen, YELLOW, back_btn_rect)
            self.screen.blit(back_text, back_text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_btn_rect.collidepoint(mouse_pos):
                        if self.is_cli:
                            pygame.quit()
                            sys.exit()
                        else:
                            running = False
            
            pygame.display.update()