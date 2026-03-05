import pygame
import sys
import time
from settings import *
from menu import Menu
from map import Map
from levels import LEVEL1
from pacman import Pacman
from ghost import Ghost

# Ініціалізація Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 

game_map = Map(screen, LEVEL1, WIDTH, HEIGHT)
player = Pacman(210, 159) 
tile = 34

ghosts = [
    Ghost("Blinky", "blinky.png", 13*tile, 13*tile, tile, (WIDTH, 0), 2),
    Ghost("Pinky", "pinky.png", 12*tile, 13*tile, tile, (0, 0), 6),
    Ghost("Inky", "inky.png", 14*tile, 13*tile, tile, (WIDTH, HEIGHT), 10),
    Ghost("Clyde", "clyde.png", 13*tile, 13*tile, tile, (0, HEIGHT), 14)
]

def run_game():
    score = 0
    lives = 3
    start_ticks = time.time() #
    
    while True:
        elapsed = (time.time() - start_ticks) % 30
        global_mode = "STUNNED" if elapsed > 20 else "CHASE"

        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        
        game_map.draw_map()
        player.update(game_map)

        # Координати для логіки привидів
        blinky_pos = (ghosts[0].rect.centerx, ghosts[0].rect.centery)

        for ghost in ghosts:
            # ТУТ ПЕРЕДАЄТЬСЯ 4 ЗНАЧЕННЯ
            ghost.update(player, game_map, blinky_pos, global_mode)
            
            if player.rect.colliderect(ghost.rect):
                lives -= 1
                pygame.time.delay(1000)
                if lives > 0:
                    player.rect.topleft = (210, 159)
                    player.direction = (0, 0)
                else:
                    return

        # ЗБІР КРАПОК: Відступ на рівні циклу 'for'
        points = game_map.collision_with_objects(player.rect.centerx, player.rect.centery)
        score += points

        player.draw(screen)
        for ghost in ghosts: ghost.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    menu = Menu(screen)
    if menu.display_main_menu() == "start_game":
        run_game()