import pygame
import sys
from settings import *
from menu import Menu

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

def run_game():
    while True:
        screen.fill(BLACK)
        pygame.display.set_caption("Game Running...")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

def main():
    menu = Menu(screen)
    action = menu.display_main_menu()

    if action == "start_game":
        run_game()

if __name__ == "__main__":
    main()