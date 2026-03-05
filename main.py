import pygame
import sys
import time
from settings import *
from menu import Menu
from map import Map
from pacman import Pacman
from ghost import Ghost
from energizer import Energizer
from cli import *

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
player = Pacman(PLAYER_X, PLAYER_Y) 

def run_game(selected_level, selected_color):
    score = 0
    energizer = Energizer()
    game_map = Map(screen, selected_level, selected_color, WIDTH, HEIGHT)

    while True:
        # Очищення 
        screen.fill(BLACK)
        
        # Відображення рахунку в заголовку вікна
        pygame.display.set_caption(f"Pac-Man | Score: {score}")

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

        energizer.update()
        
        # Перевірка на з'їдання точок/енерджайзерів
        # Використовуємо центр спрайта для більш точного поїдання
        points, is_energizer = game_map.collision_with_objects(player.rect.centerx, player.rect.centery)
        score += points

        if is_energizer:
            energizer.activate()

        # --- МАЛЮВАННЯ ---
        player.draw(screen)
        for ghost in ghosts: ghost.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def main():
    args = parse_args()
    selected_color = COLOR_MAPPING.get(args.color)

    if args.level is not None:
        selected_level = LEVEL_MAPPING.get(args.level)
        print(f"Starting Game via CLI: Level {args.level}, Color {args.color}")
        run_game(selected_level, selected_color)
    else:
        # Створюємо меню
        menu = Menu(screen)
    
        # Викликаємо головне меню
        action, selected_level, selected_color  = menu.display_main_menu()

        if action == "start_game":
            run_game(selected_level, selected_color)
        elif action == "quit": # Додано для коректного виходу з меню
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    menu = Menu(screen)
    if menu.display_main_menu() == "start_game":
        run_game()