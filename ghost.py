import pygame
import os
import time
import random

class Ghost:
    def __init__(self, name, filename, x, y, tile_size, scatter_pos, release_delay=0):
        self.name = name
        self.tile_size = tile_size
        
        # Завантаження скінів
        full_path = os.path.join("assets", filename)
        blue_path = os.path.join("assets", "blue_ghost.png")
        self.normal_image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (tile_size, tile_size))
        self.blue_image = pygame.transform.scale(pygame.image.load(blue_path).convert_alpha(), (tile_size, tile_size))
        
        self.image = self.normal_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.exit_speed = 3 # Швидкість виходу з будиночка
        self.direction = (0, -self.speed)
        
        self.mode = "WAITING"
        self.release_delay = release_delay
        self.start_time = time.time()
        self.mode_timer = 0

    def update(self, player, game_map, blinky_pos, global_mode):
        current_time = time.time()

        if self.mode == "WAITING":
            if current_time - self.start_time >= self.release_delay:
                self.mode = "EXITING"
            return

        # ШВИДКИЙ ВИХІД КРІЗЬ СТІНИ
        if self.mode == "EXITING":
            target_x = 13 * self.tile_size
            target_y = 10 * self.tile_size # Точка в коридорі

            if abs(self.rect.x - target_x) > 2:
                self.rect.x += self.exit_speed if self.rect.x < target_x else -self.exit_speed
            
            if self.rect.y > target_y:
                self.rect.y -= self.exit_speed
            else:
                self.mode = "CHASE" # Тільки тепер вмикаємо логіку стін
                self.mode_timer = current_time
            return

        # ГЛОБАЛЬНІ РЕЖИМИ
        if global_mode == "STUNNED":
            self.image = self.blue_image #
            # Дрижання
            self.rect.x += random.randint(-1, 1)
            self.rect.y += random.randint(-1, 1)
        else:
            self.image = self.normal_image
            self.move_logic(player, game_map, blinky_pos)

    def move_logic(self, player, game_map, blinky_pos):
        # Сувора перевірка стін після виходу
        if not game_map.can_move(self.rect.x + self.direction[0] + 17, self.rect.y + self.direction[1] + 17):
            possible_dirs = [(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)]
            best_dir = self.direction
            min_dist = float('inf')
            for d in possible_dirs:
                if d == (-self.direction[0], -self.direction[1]): continue
                if game_map.can_move(self.rect.x + d[0] + 17, self.rect.y + d[1] + 17):
                    dist = ((self.rect.x + d[0] - player.rect.centerx)**2 + (self.rect.y + d[1] - player.rect.centery)**2)**0.5
                    if dist < min_dist:
                        min_dist, best_dir = dist, d
            self.direction = best_dir

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)