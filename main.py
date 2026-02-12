import pygame
import sys
from settings import *
from menu import Menu
from map import Map
from levels import LEVEL1
from pacman import Pacman

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
activeLevel = LEVEL1
game_map = Map(screen, activeLevel, WIDTH, HEIGHT)
player = Pacman(100, 100)
def run_game():
    while True:
        screen.fill(BLACK)
        pygame.display.set_caption("Game Running...")
        game_map.draw_map()
        player.update(game_map)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        player.draw(screen)

def main():
    menu = Menu(screen)
    action = menu.display_main_menu()

    if action == "start_game":
        run_game()

if __name__ == "__main__":
    main()