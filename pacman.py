import pygame

class Pacman:
    def __init__(self, x, y):
        try:
            self.original_image = pygame.image.load("assets/pacman.png")
        except:
            self.original_image = pygame.Surface((34, 34), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (255, 255, 0), (17, 17), 17)
            
        # Збільшуємо до 34х34, щоб він щільно сидів у коридорі
        self.original_image = pygame.transform.scale(self.original_image, (34, 34))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.speed = 2 
        self.direction = (0, 0) 
        self.next_direction = (0, 0)

    def can_move_to(self, x, y, game_map):
        # Перевіряємо тільки одну точку — ПЕРЕД Пакменом по центру його руху
        # Якщо перед носом не стіна — він їде. Це виключає застрягання боками.
        check_x = x + 17 + (self.direction[0] * 10 if self.direction[0] != 0 else 0)
        check_y = y + 17 + (self.direction[1] * 10 if self.direction[1] != 0 else 0)
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
            target_x = self.rect.x + self.next_direction[0] * 10
            target_y = self.rect.y + self.next_direction[1] * 10
            if game_map.can_move(target_x + 17, target_y + 17):
                # Якщо ми близько до центру клітинки — «стрибаємо» в колію
                if abs(self.rect.centerx - tile_center_x) < 8 and abs(self.rect.centery - tile_center_y) < 8:
                    self.direction = self.next_direction
                    self.rect.centerx, self.rect.centery = tile_center_x, tile_center_y

        # 2. Рух + Жорстка фіксація на рейках
        new_x = self.rect.x + self.direction[0]
        new_y = self.rect.y + self.direction[1]

        if self.can_move_to(new_x, new_y, game_map):
            self.rect.x = new_x
            self.rect.y = new_y
            
            # МАГНІТ: не даємо йому зміщуватися вбік від центральної лінії
            if self.direction[0] != 0: self.rect.centery = tile_center_y # Їде горизонтально — фіксуємо Y
            if self.direction[1] != 0: self.rect.centerx = tile_center_x # Їде вертикально — фіксуємо X
        else:
            self.direction = (0, 0)
            # При зупинці вирівнюємо чітко по центру плитки
            self.rect.centerx, self.rect.centery = tile_center_x, tile_center_y

        self.rotate_sprite()

    def rotate_sprite(self):
        # (Код повороту залишається таким самим)
        if self.direction == (-self.speed, 0):
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction == (self.speed, 0):
            self.image = self.original_image
        elif self.direction == (0, -self.speed):
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == (0, self.speed):
            self.image = pygame.transform.rotate(self.original_image, 270)

    def draw(self, screen):
        screen.blit(self.image, self.rect)