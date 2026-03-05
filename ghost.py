import pygame
import os
import time
import random

class Ghost:
    def __init__(self, name, filename, x, y, tile_size, scatter_pos, release_delay=0):
        self.name = name
        self.tile_size = tile_size
        self.spawn_pos = (x + tile_size // 2, y + tile_size // 2)

        # ВИПРАВЛЕНО: Зменшуємо розмір привида до 80% від тайла
        self.draw_size = int(tile_size * 0.8)
        
        base_name = filename.split('.')[0]

        self.normal_frames = [
            self.load_and_scale(f"{base_name}.png"),
            self.load_and_scale(f"{base_name}_2.png")
        ]

        self.blue_frames = [
            self.load_and_scale("blue_ghost.png"),
            self.load_and_scale("blue_ghost_2.png")
        ]

        self.white_frames = [
            self.load_and_scale("white_ghost.png"),
            self.load_and_scale("white_ghost_2.png")
        ]
        self.eyes_image = self.load_and_scale("eyes.png")

        # Параметри анімації
        self.frame_index = 0
        self.anim_speed = 0.15
        self.anim_timer = 0
    
        self.image = self.normal_frames[0]
        self.rect = self.image.get_rect(center=self.spawn_pos)

        self.speed = 2
        self.stunned_speed = 1
        self.exit_speed = 2
        self.return_speed = 4
        self.direction = (0, -self.speed)
        
        self.mode = "WAITING"
        self.release_delay = release_delay
        self.is_vulnerable = False
        self.start_time = time.time()
    
    def update(self, player, game_map, blinky_pos, vulnerability_expiring=False):
        self.update_animation()
        current_time = time.time()

        if self.mode == "RETURNING":
            self.image = self.eyes_image
            self.fly_home()
            return
        
        if self.is_vulnerable:
            if vulnerability_expiring:
                if int(current_time * 5) % 2 == 0:
                    current_frames = self.white_frames
                else:
                    current_frames = self.blue_frames
            else:
                current_frames = self.blue_frames
                
            self.image = current_frames[self.frame_index]
            
        else:
            self.image = self.normal_frames[self.frame_index]
        
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

        self.move_logic(player, game_map, blinky_pos, is_vulnerable=self.is_vulnerable)

    def start_vulnerable(self):
       if self.mode != "RETURNING" and not self.is_vulnerable:
            self.is_vulnerable = True
            if self.mode == "CHASE":
                self.reverse_direction()


    def stop_vulnerable(self):
        self.is_vulnerable = False
            
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

    def reset(self, instant=False):
        if instant:
            self.rect.center = self.spawn_pos
            self.mode = "WAITING"
            self.start_time = time.time()
            self.direction = (0, -self.speed)
            self.is_vulnerable = False
        else:
            self.mode = "RETURNING"
            self.is_vulnerable = False

    def fly_home(self):
        target_x, target_y = self.spawn_pos
        dist = self.calculate_distance(self.rect.centerx, self.rect.centery, target_x, target_y)
        
        if dist > self.return_speed:
            dx = (target_x - self.rect.centerx) / dist
            dy = (target_y - self.rect.centery) / dist
        
            self.rect.x += dx * self.return_speed
            self.rect.y += dy * self.return_speed
        else: # Прилетів
            self.rect.center = self.spawn_pos
            self.mode = "WAITING"
            self.start_time = time.time()

    def handle_player_collision(self):
        if self.mode == "RETURNING": 
            return 0, False
        
        if self.is_vulnerable: # Помер і летить додому
            self.is_vulnerable = False
            self.reset(instant=False)
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
    
    def load_and_scale(self, name):
        path = os.path.join("assets", name)
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), (self.draw_size, self.draw_size))
    
    def update_animation(self):
        self.anim_timer += self.anim_speed
        if self.anim_timer >= 2:
            self.anim_timer = 0
        self.frame_index = int(self.anim_timer)

    def draw(self, screen):
        screen.blit(self.image, self.rect)