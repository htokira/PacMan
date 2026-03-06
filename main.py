import pygame
import sys
from settings import *
from menu import Menu
from map import Map
from pacman import Pacman
from ghost import Ghost
from energizer import Energizer
from cli import *
from screens import WinScreen, GameOverScreen

#  Ініціалізація Pygame: запуск двигуна та налаштування графічного вікна
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# Спроба завантажити фірмовий шрифт у стилі Pac-Man
try:
    UI_FONT = pygame.font.Font("fonts/Emulogic-font.ttf", 20)
except:
    UI_FONT = pygame.font.SysFont("Arial", 20)

def process_collisions(player, ghosts, game_map, energizer):
    """
    Обробляє зіткнення у грі з об'єктами карти та привидами.
    
    Перевіряє взаємодію гравця з крапками, енерджайзерами та привидами,
    оновлює стан енерджайзера та розраховує отримані бали.

    Args:
        player (Pacman): Об'єкт гравця для перевірки колізій.
        ghosts (list): Список об'єктів Ghost, присутніх на рівні.
        game_map (Map): Об'єкт карти для взаємодії з предметами.
        energizer (Energizer): Об'єкт для керування станом вразливості привидів.

    Returns:
        tuple: (total_points, death_occurred), де:
            total_points (int) — кількість балів, зароблених за поточний кадр;
            death_occurred (bool) — True, якщо гравець загинув від зіткнення з привидом, інакше - False.
    """
    total_points = 0
    death_occurred = False

    # Обробка зіткнень з крапками та енерджайзерами
    points, is_energizer = game_map.collision_with_objects(player.rect.centerx, player.rect.centery)
    total_points += points
    
    if is_energizer:
        energizer.activate()
        for ghost in ghosts:
            ghost.start_vulnerable()

    # Обробка зіткнень з привидами
    for ghost in ghosts:
        if player.rect.colliderect(ghost.rect):
            ghost_eaten, killed = ghost.handle_player_collision()
            
            if ghost_eaten:
                total_points += energizer.get_next_ghost_score()

            if killed:
                death_occurred = True
                
    return total_points, death_occurred

def draw_ui(screen, score, lives):
    """
    Відображає інтерфейс користувача у нижній частині екрана під час гри.
    
    Рендерить текстові поверхні та малює роздільну лінію під ігровим полем.

    Args:
        screen (pygame.Surface): Поверхня екрана для малювання.
        score (int): Поточний рахунок гравця.
        lives (int): Поточна кількість житів гравця.
    """
    score_surface = UI_FONT.render(f"SCORE: {score}", True, WHITE)
    lives_surface = UI_FONT.render(f"LIVES: {lives}", True, WHITE)
    
    padding = 20
    ui_y_position = HEIGHT - 45 

    screen.blit(score_surface, (padding, ui_y_position))
    
    lives_x = WIDTH - lives_surface.get_width() - padding
    screen.blit(lives_surface, (lives_x, ui_y_position))
    
    pygame.draw.line(screen, WHITE, (0, HEIGHT - 65), (WIDTH, HEIGHT - 65), 2)

def run_game(selected_level, selected_color, is_cli=False, infinite_mode=False):
    """
    Запускає основний ігровий цикл для конкретного рівня.

    Створює екземпляри гравця, привидів та карти, оновлює їхній стан кожного кадру
    та обробляє умови перемоги або поразки.

    Args:
        selected_level (list): Матриця даних вибраного рівня.
        selected_color (tuple): RGB колір стін лабіринту.
        is_cli (bool): Чи була гра запущена через аргументи командного рядка.
        infinite_mode (bool): Якщо True, рівень перезапускається після збору всіх крапок.
    """
    score = 0
    lives = 3
    
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
        # Обробка подій
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        
        # Оновлення об'єктів
        pygame.display.set_caption(f"Pac-Man | Score: {score} | Lives: {lives}")
        game_map.draw_map()

        draw_ui(screen, score, lives)

        player.update(game_map)
        energizer.update()
        is_expiring = energizer.is_about_to_expire()

        if not energizer.is_active():
            for ghost in ghosts:
                ghost.stop_vulnerable()
                
        for ghost in ghosts:  
            ghost.update(player, game_map, ghosts[0].rect.center, vulnerability_expiring=is_expiring)
        
        added_score, is_dead = process_collisions(player, ghosts, game_map, energizer)
        score += added_score

        if game_map.is_clear(): 
            if infinite_mode:
                game_map.reset_map()
            else:
                win_scr = WinScreen(screen, score, is_cli=is_cli)
                win_scr.display()
                return

        if is_dead:
            lives -= 1
            energizer.deactivate()
            if lives <= 0:
                game_over = GameOverScreen(screen, score, is_cli=is_cli)
                game_over.display()
                return
            
            player.rect.topleft = (PLAYER_X, PLAYER_Y)
            player.direction = (0, 0)
            for ghost in ghosts:
                ghost.reset(instant=True)
            pygame.time.delay(1000)

        # Малювання
        player.draw(screen)
        for ghost in ghosts: 
            ghost.draw(screen)

        pygame.display.flip()
        clock.tick(60)

def main():
    """
    Точка входу в програму.
    
    Вирішує, чи запускати гру відразу (режим CLI), чи відображати головне меню.
    Керує переходом між меню та ігровим процесом.
    """
    args = parse_args()
    menu = Menu(screen)

    selected_level = None
    selected_color = None
    is_cli = args.level is not None

    if is_cli:
        selected_color = COLOR_MAPPING.get(args.color)
        selected_level = LEVEL_MAPPING.get(args.level)
        run_game(selected_level, selected_color, is_cli=True)
        pygame.quit()
        sys.exit()
    
    while True:
        if selected_level is None and selected_color is None:
            action_data = menu.display_main_menu()
        
        # Перевірка структури відповіді меню
        if isinstance(action_data, tuple) and len(action_data) == 4:
            action, selected_level, selected_color, inf_mode = action_data
            if action == "start_game":
                run_game(selected_level, selected_color, is_cli=False, infinite_mode=inf_mode)
            elif action == "quit":
                pygame.quit(); sys.exit()

        selected_level = None
        selected_color = None

if __name__ == "__main__":
    main()