import pygame

class Pacman:
    def __init__(self, x, y):
        self.size = (27, 27)
        self.sprites = {
            "left":  self.load_frames("pacman_left"),
            "right": self.load_frames("pacman_right"),
            "up":    self.load_frames("pacman_up"),
            "down":  self.load_frames("pacman_down")
        }

        self.look_direction = "right" 
        self.frame_index = 0
        self.anim_speed = 0.2
        self.anim_timer = 0
            
        self.image = self.sprites[self.look_direction][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.speed = 2 
        self.direction = (0, 0) 
        self.next_direction = (0, 0)

    def can_move_to(self, x, y, game_map):
        # Перевіряємо тільки одну точку — ПЕРЕД Пакменом по центру його руху
        # Якщо перед носом не стіна — він їде. Це виключає застрягання боками.
        dx = 0 if self.direction[0] == 0 else 1 if self.direction[0] > 0 else -1
        dy = 0 if self.direction[1] == 0 else 1 if self.direction[1] > 0 else -1
        
        check_x = x + 13 + dx * 8
        check_y = y + 13 + dy * 8

        if dx != 0:  # Тільки коли рухаємося ліво/право
            if check_x < 0:
                check_x += game_map.width
            elif check_x >= game_map.width:
                check_x -= game_map.width

        return game_map.can_move(check_x, check_y)

    def update(self, game_map):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  self.next_direction = (-self.speed, 0)
        if keys[pygame.K_RIGHT]: self.next_direction = (self.speed, 0)
        if keys[pygame.K_UP]:    self.next_direction = (0, -self.speed)
        if keys[pygame.K_DOWN]:  self.next_direction = (0, self.speed)

        # Центр плитки (ось доріжки)
        tile_center_x = (self.rect.centerx // game_map.w) * game_map.w + game_map.w // 2
        tile_center_y = (self.rect.centery // game_map.h) * game_map.h + game_map.h // 2

        # 1. Поворот: дозволяємо тільки якщо ми в центрі перехрестя
        if self.next_direction != self.direction:
            # Перевіряємо точку повороту
            target_x = self.rect.x + self.next_direction[0] * 8
            target_y = self.rect.y + self.next_direction[1] * 8
            if game_map.can_move(target_x + 13, target_y + 13):
                # Якщо ми близько до центру клітинки — «стрибаємо» в колію
                if abs(self.rect.centerx - tile_center_x) < 6 and abs(self.rect.centery - tile_center_y) < 6:
                    self.direction = self.next_direction
                    self.rect.centerx, self.rect.centery = tile_center_x, tile_center_y
                    self.update_look_direction()

        # 2. Рух + Жорстка фіксація на рейках
        new_x = self.rect.x + self.direction[0]
        new_y = self.rect.y + self.direction[1]

        if self.can_move_to(new_x, new_y, game_map):
            self.rect.x = new_x
            self.rect.y = new_y
            
            # МАГНІТ: не даємо йому зміщуватися вбік від центральної лінії
            if self.direction[0] != 0: self.rect.centery = tile_center_y # Їде горизонтально — фіксуємо Y
            if self.direction[1] != 0: self.rect.centerx = tile_center_x # Їде вертикально — фіксуємо X

            if self.rect.centerx < 0:
                self.rect.centerx += game_map.width
            elif self.rect.centerx >= game_map.width:
                self.rect.centerx -= game_map.width
        else:
            self.direction = (0, 0)
            # При зупинці вирівнюємо чітко по центру плитки
            self.rect.centerx, self.rect.centery = tile_center_x, tile_center_y

        self.update_animation()
    
    def load_frames(self, prefix):
        """
        Завантажує кадри анімації з папки.

        Args:
            prefix (str): Текстовий префікс для назви файлів спрайтів.

        Returns:
            list: Список об'єктів pygame.Surface, що містять завантажені та масштабовані кадри.
        """
        frames = []
        for i in range(1, 4):
            path = f"assets/pacman/{prefix}_{i}.png"
            try:
                img = pygame.image.load(path).convert_alpha()
                frames.append(pygame.transform.scale(img, self.size))
            except:
                surf = pygame.Surface(self.size, pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 255, 0), (13, 13), 13 - i*2)
                frames.append(surf)
        return frames
    
    def update_animation(self):
        """
        Керує циклом анімації Пакмена.
        """
        if self.direction != (0, 0): # Програється анімація
            self.anim_timer += self.anim_speed

            if self.anim_timer >= 4:
                self.anim_timer = 0
                
            animation_sequence = [0, 1, 2, 1] # Анімація 1 - 2 - 3 - 2
            self.frame_index = animation_sequence[int(self.anim_timer)]
        else: # Відсутня анімація
            self.frame_index = 2

        self.image = self.sprites[self.look_direction][self.frame_index]
    
    def update_look_direction(self):
        """
        Визначає напрямок Пакмена для вибору відповідного набору спрайтів.
        """
        if self.direction == (-self.speed, 0): self.look_direction = "left"
        elif self.direction == (self.speed, 0): self.look_direction = "right"
        elif self.direction == (0, -self.speed): self.look_direction = "up"
        elif self.direction == (0, self.speed): self.look_direction = "down"

    def draw(self, screen):
        screen.blit(self.image, self.rect)