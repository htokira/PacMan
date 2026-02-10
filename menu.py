import pygame
import sys
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('fonts/Emulogic-font.ttf', 75)
        self.button_font = pygame.font.Font('fonts/Emulogic-font.ttf', 40)

        # Menu title
        self.title_text = self.font.render("PAC-MAN", True, WHITE)
        self.title_rect = self.title_text.get_rect(center = (WIDTH // 2, 150))

        # Start game button
        self.button_rect = pygame.Rect(0, 0, 200, 60)
        self.button_rect.center = (WIDTH // 2, 350)

        self.btn_text = self.button_font.render("PLAY", True, BLACK)
        self.btn_text_rect = self.btn_text.get_rect(center=self.button_rect.center)

    def draw_menu(self):
        self.screen.fill(BLACK)   
        self.screen.blit(self.title_text, self.title_rect)
        pygame.draw.rect(self.screen, YELLOW, self.button_rect)
        self.screen.blit(self.btn_text, self.btn_text_rect)

    def display_main_menu(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.draw_menu()

            # Event start game or quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.button_rect.collidepoint(mouse_pos):
                        return "start_game"

            pygame.display.update()