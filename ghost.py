import pygame
import os
import time
import random

class Ghost:
    def __init__(self, name, filename, x, y, tile_size, scatter_pos, release_delay=0):
        self.name = name
        self.tile_size = tile_size
        
        # ВИПРАВЛЕНО: Зменшуємо розмір привида до 80% від тайла
        self.draw_size = int(tile_size * 0.8)
        
        full_path = os.path.join("assets", filename)
        blue_path = os.path.join("assets", "blue_ghost.png")
        
        # Масштабуємо зображення під новий розмір
        self.normal_image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (self.draw_size, self.draw_size))
        self.blue_image = pygame.transform.scale(pygame.image.load(blue_path).convert_alpha(), (self.draw_size, self.draw_size))
        
        self.image = self.normal_image
        
        # ВИПРАВЛЕНО: Центруємо хитбокс привида всередині тайла
        offset = (tile_size - self.draw_size) // 2
        self.rect = self.image.get_rect(topleft=(x + offset, y + offset))
        
        self.speed = 2
        self.exit_speed = 3
        self.direction = (0, -self.speed)
        
        self.mode = "WAITING"
        self.release_delay = release_delay
        self.start_time = time.time()

    def update(self, player, game_map, blinky_pos, global_mode):
        current_time = time.time()

        if self.mode == "WAITING":
            if current_time - self.start_time >= self.release_delay:
                self.mode = "EXITING"
            return

        # --- ЖОРСТКА ЛОГІКА ВИХОДУ ---
        if self.mode == "EXITING":
            # 1. Центр проходу (біла лінія)
            target_center_x = 10 * self.tile_size + (self.tile_size // 2)
            
            # 2. ЛІНІЯ СТОП: Рівень білої полоски (9-й тайл)
            gate_y = 8 * self.tile_size 

            # КРОК А: Вирівнювання (спочатку тільки вбік)
            if abs(self.rect.centerx - target_center_x) > 2:
                self.rect.x += self.exit_speed if self.rect.centerx < target_center_x else -self.exit_speed
                return # НЕ ЙДЕМО ВГОРУ, поки не стали по центру

            # КРОК Б: Рух вгору ТІЛЬКИ до білої лінії
            if self.rect.y > gate_y:
                self.rect.y -= self.exit_speed
                return # Ігноруємо стіни ТІЛЬКИ тут
            else:
                # МИТТЄВА ЗМІНА РЕЖИМУ: тепер привид бачить стіни
                self.mode = "CHASE"
                self.rect.y = gate_y # Фіксуємо на рівні проходу
                # Не робимо return, щоб одразу пішла перевірка стін нижче

        # --- РЕЖИМ ПІСЛЯ ВИХОДУ: СТІНИ НЕПРОХІДНІ ---
        if global_mode == "STUNNED":
            self.image = self.blue_image
    # Незначне випадкове зміщення без зміни основних координат
            self.rect.x += random.randint(-1, 1)
            self.rect.y += random.randint(-1, 1)
    # move_logic НЕ викликаємо!
        else:
            self.image = self.normal_image
            self.move_logic(player, game_map, blinky_pos)
    def move_logic(self, player, game_map, blinky_pos):
        # ВИПРАВЛЕНО: Використовуємо динамічний центр для перевірки колізій
        check_offset = self.draw_size // 2
        
        if not game_map.can_move(self.rect.x + self.direction[0] + check_offset, self.rect.y + self.direction[1] + check_offset):
            possible_dirs = [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
            best_dir = self.direction
            min_dist = float('inf')
            for d in possible_dirs:
                if d == (-self.direction[0], -self.direction[1]): continue
                # Також використовуємо check_offset тут
                if game_map.can_move(self.rect.x + d[0] + check_offset, self.rect.y + d[1] + check_offset):
                    dist = ((self.rect.x + d[0] - player.rect.centerx)**2 + (self.rect.y + d[1] - player.rect.centery)**2)**0.5
                    if dist < min_dist:
                        min_dist, best_dir = dist, d
            self.direction = best_dir

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)