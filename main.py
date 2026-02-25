import pygame
import sys
from settings import *
from menu import Menu
from map import Map
from levels import LEVEL1
from pacman import Pacman

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

def run_game():
    score = 0
    while True:
        # Очищення екрану
        screen.fill(BLACK)
        
        # Відображення рахунку в заголовку вікна
        pygame.display.set_caption(f"Pac-Man | Score: {score}")

        # --- ЛОГІКА ТА ОНОВЛЕННЯ ---
        
        # Обробка подій (вихід з гри)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Малюємо карту (стіни та точки)
        game_map.draw_map()
        
        # Оновлюємо Пакмена (рух, анімація та "рейкова" логіка)
        player.update(game_map)
        
        # Перевірка на з'їдання точок/енерджайзерів
        # Використовуємо центр спрайта для більш точного поїдання
        points = game_map.collision_with_objects(player.rect.centerx, player.rect.centery)
        score += points

        # --- МАЛЮВАННЯ ---
        player.draw(screen)

        # Оновлення екрану
        pygame.display.flip()
        
        # Обмеження FPS (60 кадрів на секунду)
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