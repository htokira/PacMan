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
        
        # Масштабуємо зображеннія під новий розмір
        self.normal_image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (self.draw_size, self.draw_size))
        self.blue_image = pygame.transform.scale(pygame.image.load(blue_path).convert_alpha(), (self.draw_size, self.draw_size))
        
        self.image = self.normal_image

        self.rect = self.image.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
        
        self.speed = 2
        self.stunned_speed = 1
        self.exit_speed = 2
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

        # ЛОГІКА ВИХОДУ
        if self.mode == "EXITING":
            # 1. Центр проходу (біла лінія)
            target_center_x = 10 * self.tile_size + (self.tile_size // 2)
            
            # 2. ЛІНІЯ СТОП: Рівень білої полоски (9-й тайл)
            gate_y = 8 * self.tile_size 

            # КРОК А: Вирівнювання
            dist_x = target_center_x - self.rect.centerx
            if abs(dist_x) > self.exit_speed:
                self.rect.x += self.exit_speed if dist_x > 0 else -self.exit_speed
                return # НЕ ЙДЕМО ВГОРУ, поки не стали по центру
            else:
                self.rect.centerx = target_center_x

            # КРОК Б: Рух вгору ТІЛЬКИ до білої лінії
            if self.rect.y > gate_y:
                self.rect.y -= self.exit_speed
                return # Ігноруємо стіни ТІЛЬКИ тут
            else:
                # МИТТЄВА ЗМІНА РЕЖИМУ: тепер привид бачить стіни
                self.mode = "CHASE"
                self.rect.y = gate_y - (self.tile_size // 2)
                self.direction = (0, -self.speed)

        # --- РЕЖИМ ПІСЛЯ ВИХОДУ: СТІНИ НЕПРОХІДНІ ---
        if global_mode == "STUNNED":
            self.image = self.blue_image
            self.move_logic(player, game_map, blinky_pos, is_vulnerable=True)
        else:
            self.image = self.normal_image
            self.move_logic(player, game_map, blinky_pos, is_vulnerable=False)

    def move_logic(self, player, game_map, blinky_pos, is_vulnerable=False):
        current_speed = self.stunned_speed if is_vulnerable else self.speed
        check_offset = self.draw_size // 2  

        direction_x, direction_y = self.normalize_direction(current_speed)
        
        next_x = self.rect.x + direction_x + check_offset
        next_y = self.rect.y + direction_y + check_offset

        if not game_map.can_move(next_x,next_y):
            self.direction = self.choose_direction(player, game_map, check_offset, current_speed, is_vulnerable)
            direction_x, direction_y = self.direction

        self.rect.x += direction_x
        self.rect.y += direction_y

    def reset(self):
        spawn_x = self.rect.centerx // self.tile_size
        spawn_y = self.rect.centery // self.tile_size
        self.rect.center = (spawn_x * self.tile_size + self.tile_size // 2, 
                            spawn_y * self.tile_size + self.tile_size // 2)
        self.mode = "WAITING"
        self.start_time = time.time()
        self.image = self.normal_image

    def handle_player_collision(self, is_vulnerable):
        if is_vulnerable:
            self.reset()
            return 200, False
        return 0, True

    def normalize_direction(self, speed):
        dir_x = speed if self.direction[0] > 0 else -speed if self.direction[0] < 0 else 0
        dir_y = speed if self.direction[1] > 0 else -speed if self.direction[1] < 0 else 0
        return dir_x, dir_y

    def choose_direction(self, player, game_map, check_offset, current_speed, is_vulnerable):
        possible_dirs = [(current_speed, 0), (-current_speed, 0), (0, current_speed), (0, -current_speed)]
       
        back_dir = (-self.direction[0], -self.direction[1])

        valid_dirs = []
        for d in possible_dirs:
            if d[0] == back_dir[0] and d[1] == back_dir[1] and len(possible_dirs) > 1:
                continue
            
            if game_map.can_move(self.rect.x + d[0] + check_offset, self.rect.y + d[1] + check_offset):
                valid_dirs.append(d)

        if not valid_dirs:
            return back_dir
        
        if is_vulnerable:
            return random.choice(valid_dirs)
        else: 
            return self.find_closest_direction(valid_dirs, player)
        
    def find_closest_direction(self, valid_dirs, player):
        best_dir = valid_dirs[0]
        min_dist = float('inf')

        for d in valid_dirs:
            dist = self.calculate_distance(self.rect.x + d[0], self.rect.y + d[1], player.rect.centerx, player.rect.centery)
            
            if dist < min_dist:
                min_dist, best_dir = dist, d
        
        return best_dir
    
    def reverse_direction(self):
        self.direction = (-self.direction[0], -self.direction[1])
    
    def calculate_distance(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def draw(self, screen):
        screen.blit(self.image, self.rect)