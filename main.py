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

def process_collisions(player, ghosts, game_map, energizer):
    total_points = 0
    death_occurred = False

    points, is_energizer = game_map.collision_with_objects(player.rect.centerx, player.rect.centery)
    total_points += points
    
    if is_energizer:
        energizer.activate()
        for ghost in ghosts:
            if ghost.mode not in ["WAITING", "EXITING"]:
                ghost.reverse_direction()

    for ghost in ghosts:
        if player.rect.colliderect(ghost.rect):
            points, killed = ghost.handle_player_collision(energizer.is_active())
            total_points += points
            if killed:
                death_occurred = True
                
    return total_points, death_occurred

def run_game(selected_level, selected_color):
    score = 0
    lives = 3
    start_ticks = time.time() # Ініціалізація для global_mode
    
    # Ініціалізація карти та гравця всередині функції
    game_map = Map(screen, selected_level, selected_color, WIDTH, HEIGHT)

    tile = 34

    player = Pacman(PLAYER_X, PLAYER_Y) 
    ghosts = [
        Ghost("Blinky", "blinky.png", 11*tile, 9*tile, tile, (WIDTH, 0), 2),
        Ghost("Pinky", "pinky.png", 9*tile, 9*tile, tile, (0, 0), 6),
        Ghost("Inky", "inky.png", 12*tile, 9*tile, tile, (WIDTH, HEIGHT), 10),
        Ghost("Clyde", "clyde.png", 10*tile, 9*tile, tile, (0, HEIGHT), 14)
    ]

    energizer = Energizer()

    while True:
        # 1. Розрахунок часу та режиму
        if energizer.is_active():
            global_mode = "STUNNED"
        else:
            elapsed = (time.time() - start_ticks) % 30
            global_mode = "CHASE" if elapsed < 20 else "SCATTER"

        # 2. Обробка подій
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        
        # 3. Оновлення об'єктів
        pygame.display.set_caption(f"Pac-Man | Score: {score} | Lives: {lives}")
        game_map.draw_map()

        player.update(game_map)
        energizer.update()

        for ghost in ghosts:  
            ghost.update(player, game_map, ghosts[0].rect.center, global_mode)
        
        added_score, is_dead = process_collisions(player, ghosts, game_map, energizer)
        score += added_score

        if is_dead:
            lives -= 1
            if lives <= 0:
                return  # Game Over
            
            player.rect.topleft = (PLAYER_X, PLAYER_Y)
            player.direction = (0, 0)
            for ghost in ghosts:
                ghost.reset(instant=True)
            pygame.time.delay(1000)
            
        # 5. Малювання
        player.draw(screen)
        for ghost in ghosts: 
            ghost.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def main():
    args = parse_args()
    selected_color = COLOR_MAPPING.get(args.color)

    if args.level is not None:
        selected_level = LEVEL_MAPPING.get(args.level)
        run_game(selected_level, selected_color)
    else:
        menu = Menu(screen)
        # Отримуємо вибір з меню
        action_data = menu.display_main_menu()
        
        # Перевірка структури відповіді меню
        if isinstance(action_data, tuple) and len(action_data) == 3:
            action, selected_level, selected_color = action_data
            if action == "start_game":
                run_game(selected_level, selected_color)
            elif action == "quit":
                pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()