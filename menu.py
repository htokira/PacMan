import os
import pygame
import sys
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        # Визначаємо шлях до папки, де лежить цей файл (menu.py)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.init_fonts()
        self.init_main_menu()
        self.init_difficulty_menu()

    def init_fonts(self):
        # Будуємо шлях до файлу шрифту відносно поточної папки
        font_path = os.path.join(self.current_dir, 'fonts', 'Emulogic-font.ttf')
        
        # Перевіряємо, чи існує файл, щоб вивести зрозумілу помилку, якщо щось не так
        if not os.path.exists(font_path):
            print(f"ERROR: Font file not found at {font_path}")
            # Можна використати системний шрифт як запасний варіант
            self.font = pygame.font.SysFont('Arial', 75)
            self.button_font = pygame.font.SysFont('Arial', 40)
            self.small_button_font = pygame.font.SysFont('Arial', 25)
        else:
            self.font = pygame.font.Font(font_path, 75)
            self.button_font = pygame.font.Font(font_path, 40)
            self.small_button_font = pygame.font.Font(font_path, 25)
        
    def init_main_menu(self):
        # Title
        self.title_text = self.font.render("PAC-MAN", True, WHITE)
        self.title_rect = self.title_text.get_rect(center = (WIDTH // 2, 150))

        # Start game button
        self.button_rect = pygame.Rect(0, 0, 200, 60)
        self.button_rect.center = (WIDTH // 2, 350)
        self.btn_text = self.button_font.render("PLAY", True, BLACK)
        self.btn_text_rect = self.btn_text.get_rect(center=self.button_rect.center)

        # Difficulty button
        self.diff_btn_rect = pygame.Rect(0, 0, 250, 60)
        self.diff_btn_rect.center = (WIDTH // 2, 450)
        self.diff_text = self.small_button_font.render("DIFFICULTY", True, BLACK)
        self.diff_text_rect = self.diff_text.get_rect(center=self.diff_btn_rect.center)

        # Quit button
        self.quit_btn_rect = pygame.Rect(0, 0, 200, 60)
        self.quit_btn_rect.center = (WIDTH // 2, 550)
        self.quit_text = self.button_font.render("QUIT", True, BLACK)
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_btn_rect.center)

    def init_difficulty_menu(self):
        self.diff_title = self.button_font.render("SELECT DIFFICULTY", True, YELLOW)
        self.diff_title_rect = self.diff_title.get_rect(center=(WIDTH // 2, 100))

        # Difficulty options
        self.easy_text = self.small_button_font.render("EASY", True, WHITE)
        self.easy_rect = self.easy_text.get_rect(center=(WIDTH // 2, 220))

        self.med_text = self.small_button_font.render("MEDIUM", True, WHITE)
        self.med_rect = self.med_text.get_rect(center=(WIDTH // 2, 300))

        self.hard_text = self.small_button_font.render("HARD", True, WHITE)
        self.hard_rect = self.hard_text.get_rect(center=(WIDTH // 2, 380))
        
        # Back
        self.back_text = self.small_button_font.render("BACK", True, WHITE)
        self.back_rect = self.back_text.get_rect(center=(WIDTH // 2, 500))

    def draw_main_menu(self):
        self.screen.fill(BLACK)   
        self.screen.blit(self.title_text, self.title_rect)

        # Play button
        pygame.draw.rect(self.screen, YELLOW, self.button_rect)
        self.screen.blit(self.btn_text, self.btn_text_rect)

        # Difficulty button
        pygame.draw.rect(self.screen, YELLOW, self.diff_btn_rect)
        self.screen.blit(self.diff_text, self.diff_text_rect)

        # Quit button
        pygame.draw.rect(self.screen, YELLOW, self.quit_btn_rect)
        self.screen.blit(self.quit_text, self.quit_text_rect)

    def draw_difficulty_menu(self):
        self.screen.fill(BLACK)   
        self.screen.blit(self.diff_title, self.diff_title_rect)
        self.screen.blit(self.easy_text, self.easy_rect)
        self.screen.blit(self.med_text, self.med_rect)
        self.screen.blit(self.hard_text, self.hard_rect)
        self.screen.blit(self.back_text, self.back_rect)
        
    def display_difficulty_menu(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_difficulty_menu()

            for event in pygame.event.get():
                self.handle_quit_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.easy_rect.collidepoint(mouse_pos):
                        print("Selected EASY")
                    elif self.med_rect.collidepoint(mouse_pos):
                        print("Selected MEDIUM")
                    elif self.hard_rect.collidepoint(mouse_pos):
                        print("Selected HARD")
                    elif self.back_rect.collidepoint(mouse_pos):
                        running = False

            pygame.display.update()

    def handle_quit_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    def display_main_menu(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_main_menu()

            for event in pygame.event.get():
                self.handle_quit_event(event)
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect.collidepoint(mouse_pos):
                        return "start_game"
                        
                    if self.diff_btn_rect.collidepoint(mouse_pos):
                        self.display_difficulty_menu()

                    elif self.quit_btn_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()