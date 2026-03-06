import os
import pygame
import sys
from settings import *
from levels import *

class Menu:
    """
    Клас для керування ігровим меню.
    Відповідає за відображення головного меню та меню вибору складності, завантаження шрифтів та обробку вибору користувача.
    """
    def __init__(self, screen):
        """
        Ініціалізує об'єкт меню.

        Args:
            screen (pygame.Surface): Поверхня екрана, на якій буде малюватися меню.
        """
        self.screen = screen
        # Шлях до папки, де лежить цей файл
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.selected_level = LEVEL1
        self.selected_color = BLUE
        self.infinite_mode = False
        self.init_fonts()
        self.init_main_menu()
        self.init_difficulty_menu()

    def init_fonts(self):
        """
        Завантажує кастомний шрифт або встановлює системний як запасний.
        """
        font_path = os.path.join(self.current_dir, 'fonts', 'Emulogic-font.ttf')

        if not os.path.exists(font_path):
            print(f"ERROR: Font file not found at {font_path}")
            # Системний шрифт
            self.font = pygame.font.SysFont('Arial', 75)
            self.button_font = pygame.font.SysFont('Arial', 40)
            self.medium_button_font = pygame.font.SysFont('Arial', 35)
            self.small_button_font = pygame.font.SysFont('Arial', 25)
        else:
            self.font = pygame.font.Font(font_path, 75)
            self.button_font = pygame.font.Font(font_path, 40)
            self.medium_button_font = pygame.font.Font(font_path, 35)
            self.small_button_font = pygame.font.Font(font_path, 25)
        
    def init_main_menu(self):
        """
        Створює текстові поверхні та прямокутники для кнопок головного меню.
        """
        # Заголовок
        self.title_text = self.font.render("PAC-MAN", True, WHITE)
        self.title_rect = self.title_text.get_rect(center = (WIDTH // 2, 150))

        # Start game кнопка
        self.button_rect = pygame.Rect(0, 0, 200, 60)
        self.button_rect.center = (WIDTH // 2, 300)
        self.btn_text = self.button_font.render("PLAY", True, BLACK)
        self.btn_text_rect = self.btn_text.get_rect(center=self.button_rect.center)

        self.mode_btn_rect = pygame.Rect(0, 0, 300, 60)
        self.mode_btn_rect.center = (WIDTH // 2, 380)

        # Difficulty кнопка
        self.diff_btn_rect = pygame.Rect(0, 0, 250, 60)
        self.diff_btn_rect.center = (WIDTH // 2, 460)
        self.diff_text = self.small_button_font.render("DIFFICULTY", True, BLACK)
        self.diff_text_rect = self.diff_text.get_rect(center=self.diff_btn_rect.center)

        # Quit кнопка
        self.quit_btn_rect = pygame.Rect(0, 0, 200, 60)
        self.quit_btn_rect.center = (WIDTH // 2, 540)
        self.quit_text = self.button_font.render("QUIT", True, BLACK)
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_btn_rect.center)

    def init_difficulty_menu(self):
        """
        Створює текстові поверхні та прямокутники для меню вибору складності.
        """
        self.diff_title = self.button_font.render("SELECT DIFFICULTY", True, YELLOW)
        self.diff_title_rect = self.diff_title.get_rect(center=(WIDTH // 2, 100))

        # Опції складності
        self.easy_text = self.small_button_font.render("EASY", True, WHITE)
        self.easy_rect = self.easy_text.get_rect(center=(WIDTH // 2, 220))

        self.med_text = self.small_button_font.render("MEDIUM", True, WHITE)
        self.med_rect = self.med_text.get_rect(center=(WIDTH // 2, 300))

        self.hard_text = self.small_button_font.render("HARD", True, WHITE)
        self.hard_rect = self.hard_text.get_rect(center=(WIDTH // 2, 380))
        
        # Назад
        self.back_text = self.small_button_font.render("BACK", True, WHITE)
        self.back_rect = self.back_text.get_rect(center=(WIDTH // 2, 500))

    def draw_main_menu(self):
        """
        Малює всі елементи головного меню на екрані.
        """
        self.screen.fill(BLACK)   
        self.screen.blit(self.title_text, self.title_rect)

        # Play кнопка
        pygame.draw.rect(self.screen, YELLOW, self.button_rect)
        self.screen.blit(self.btn_text, self.btn_text_rect)

        if self.infinite_mode:
            current_bg_color = BLUE
            current_text_color = WHITE
            mode_label = "INFINITE"
        else:
            current_bg_color = YELLOW
            current_text_color = BLACK
            mode_label = "CLASSIC"

        pygame.draw.rect(self.screen, current_bg_color, self.mode_btn_rect)
        mode_text = self.medium_button_font.render(mode_label, True, current_text_color)
        mode_text_rect = mode_text.get_rect(center=self.mode_btn_rect.center)
        self.screen.blit(mode_text, mode_text_rect)

        # Difficulty кнопка
        pygame.draw.rect(self.screen, YELLOW, self.diff_btn_rect)
        self.screen.blit(self.diff_text, self.diff_text_rect)

        # Quit кнопка
        pygame.draw.rect(self.screen, YELLOW, self.quit_btn_rect)
        self.screen.blit(self.quit_text, self.quit_text_rect)

    def draw_difficulty_menu(self):
        """
        Малює всі елементи меню складності на екрані.
        """
        self.screen.fill(BLACK)   
        self.screen.blit(self.diff_title, self.diff_title_rect)
        self.screen.blit(self.easy_text, self.easy_rect)
        self.screen.blit(self.med_text, self.med_rect)
        self.screen.blit(self.hard_text, self.hard_rect)
        self.screen.blit(self.back_text, self.back_rect)
        
    def display_difficulty_menu(self):
        """
        Запускає цикл обробки подій для меню складності.
        Дозволяє користувачеві вибрати рівень або повернутися назад.
        """
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_difficulty_menu()

            for event in pygame.event.get():
                self.handle_quit_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.easy_rect.collidepoint(mouse_pos):
                        self.selected_level = LEVEL1
                        self.selected_color = BLUE
                        print("Selected EASY")
                    elif self.med_rect.collidepoint(mouse_pos):
                        self.selected_level = LEVEL2
                        self.selected_color = GREEN
                        print("Selected MEDIUM")
                    elif self.hard_rect.collidepoint(mouse_pos):
                        self.selected_level = LEVEL3
                        self.selected_color = RED
                        print("Selected HARD")
                    elif self.back_rect.collidepoint(mouse_pos):
                        running = False

            pygame.display.update()

    def handle_quit_event(self, event):
        """
        Перевіряє, чи була ініційована подія виходу з програми.

        Args:
            event (pygame.event.Event): Подія Pygame для перевірки.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    def display_main_menu(self):
        """
        Запускає цикл обробки подій для головного меню.

        Returns:
            tuple: Кортеж ("start_game", level, color, inf_mode), якщо натиснута кнопка Play.
        """
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_main_menu()

            for event in pygame.event.get():
                self.handle_quit_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(mouse_pos):
                        return "start_game", self.selected_level, self.selected_color, self.infinite_mode

                    if self.mode_btn_rect.collidepoint(mouse_pos):
                        self.infinite_mode = not self.infinite_mode
                        
                    if self.diff_btn_rect.collidepoint(mouse_pos):
                        self.display_difficulty_menu()

                    elif self.quit_btn_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()