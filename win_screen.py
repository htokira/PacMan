import os
import pygame
import sys
from settings import *

class WinScreen:
    """
    Клас для відображення екрана перемоги після завершення гри.
    """
    def __init__(self, screen, score, is_cli=False):
        """
        Ініціалізує екран перемоги.

        Args:
            screen (pygame.Surface): Поверхня для малювання елементів інтерфейсу.
            score (int): Фінальний рахунок гравця.
            is_cli (bool): Прапорець, що вказує, чи запущена гра через CLI. 
                          Впливає на текст кнопки та логіку виходу.
        """
        self.screen = screen
        self.score = score
        self.is_cli = is_cli
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.init_fonts()

    def init_fonts(self):
        """
        Завантажує шрифти для тексту. 
        """
        font_path = os.path.join(self.current_dir, 'fonts', 'Emulogic-font.ttf')
        if not os.path.exists(font_path):
            self.font = pygame.font.SysFont('Arial', 75)
            self.score_font = pygame.font.SysFont('Arial', 30)
            self.button_font = pygame.font.SysFont('Arial', 40)
        else:
            self.font = pygame.font.Font(font_path, 75)
            self.score_font = pygame.font.Font(font_path, 30)
            self.button_font = pygame.font.Font(font_path, 40)

    def display(self):
        """
        Запускає головний цикл відображення екрана перемоги.

        1. Рендерить текст перемоги та фінальний рахунок.
        2. Обробляє положення та назву кнопки (EXIT або MAIN MENU).
        3. Оновлює екран та відстежує кліки миші.
        4. Завершує роботу програми або повертає керування основному циклу гри.
        """
        win_text = self.font.render("YOU WIN!", True, GREEN) 
        win_rect = win_text.get_rect(center=(WIDTH // 2, 200))

        score_surface = self.score_font.render(f"FINAL SCORE: {self.score}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 300))

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
            self.screen.blit(score_surface, score_rect)
            
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