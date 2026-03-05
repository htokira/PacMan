import pygame
import sys
from settings import *
from menu import Menu
from map import Map
from levels import LEVEL1
from pacman import Pacman
from ghost import Ghost
import time # Обов'язково додайте цей імпорт!


# 1. Ініціалізація Pygame та екрану
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")
clock = pygame.time.Clock() 

# 2. Створення основних об'єктів
activeLevel = LEVEL1
game_map = Map(screen, activeLevel, WIDTH, HEIGHT)

# --- ВИПРАВЛЕНО ---
# Передаємо game_map, щоб Пакмен міг обрати початковий напрямок погляду
# Використовуємо координати, які потрапляють у центр коридору
player = Pacman(210, 159) 
tile = 34
tile = 34
# Центр будиночка по горизонталі — це 13-й тайл.
# Внутрішня частина по вертикалі — це приблизно 13.5 тайл.
ghosts = [
    Ghost("Blinky", "blinky.png", 13*tile, 13*tile, tile, (WIDTH, 0), 2),
    Ghost("Pinky", "pinky.png", 12*tile, 13*tile, tile, (0, 0), 6),
    Ghost("Inky", "inky.png", 14*tile, 13*tile, tile, (WIDTH, HEIGHT), 10),
    Ghost("Clyde", "clyde.png", 13*tile, 13*tile, tile, (0, HEIGHT), 14)
]
def reset_positions(player, ghosts):
    # Початкові координати Пакмена
    player.rect.topleft = (210, 159)
    player.direction = (0, 0)
    player.next_direction = (0, 0)
    
    # Початкові координати привидів (ті самі, що при створенні)
    start_coords = [(400, 300), (440, 300), (400, 340), (440, 340)]
    for i, ghost in enumerate(ghosts):
        ghost.rect.topleft = start_coords[i]
        ghost.direction = (0, -ghost.speed)
def reset_positions(player, ghosts):
    # Пакмен завжди на старт
    player.rect.topleft = (210, 159)
    player.direction = (0, 0)
    player.next_direction = (0, 0)
    
    # ПРИВИДІВ НЕ ТОРКАЄМОСЯ - вони залишаються на місці
    # (Видалено цикл скидання координат привидів)

def run_game():
    score = 0
    lives = 3
    start_ticks = time.time() # Ініціалізація часу
    
    while True:
        # Розрахунок режиму (20с погоня / 10с заціпеніння)
        elapsed = (time.time() - start_ticks) % 30
        global_mode = "STUNNED" if elapsed > 20 else "CHASE"

        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        game_map.draw_map()
        player.update(game_map)

        # Координати Блінкі для логіки інших привидів
        blinky_pos = (ghosts[0].rect.centerx, ghosts[0].rect.centery)

        # Оновлення привидів
        for ghost in ghosts:
            ghost.update(player, game_map, blinky_pos, global_mode)
            
            # Логіка зіткнення з привидом
            if player.rect.colliderect(ghost.rect):
                lives -= 1
                pygame.display.flip()
                pygame.time.delay(1000) # Пауза (всі стоять на місці)
                
                if lives > 0:
                    # Телепортуємо тільки Пакмена
                    player.rect.topleft = (210, 159)
                    player.direction = (0, 0)
                    player.next_direction = (0, 0)
                    # Привиди НЕ скидаються, вони лишаються там, де були
                else:
                    return # Game Over

        # --- ЗБІР КРАПОЧОК (Важливо: правильний відступ!) ---
        # Цей код має працювати КОЖЕН кадр
        points = game_map.collision_with_objects(player.rect.centerx, player.rect.centery)
        score += points

        # Малювання
        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)

        pygame.display.flip()
        clock.tick(60)
def main():
    # Створюємо меню
    menu = Menu(screen)
    
    # Викликаємо головне меню
    action = menu.display_main_menu()

    if action == "start_game":
        run_game()
    elif action == "quit": # Додано для коректного виходу з меню
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()