import pygame

class Pacman:
    def __init__(self, x, y):
        # Завантажуємо спрайт
        self.original_image = pygame.image.load("assets/pacman.png")
        self.original_image = pygame.transform.scale(self.original_image, (30, 30))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.speed = 3
        
        # ДЕТАЛЬ 1: Відразу задаємо рух вправо при запуску
        self.direction = (self.speed, 0) 
        self.next_direction = (self.speed, 0)

    def update(self, walls):
        keys = pygame.key.get_pressed()

        # Зчитуємо клавіші
        if keys[pygame.K_LEFT]:  self.next_direction = (-self.speed, 0)
        if keys[pygame.K_RIGHT]: self.next_direction = (self.speed, 0)
        if keys[pygame.K_UP]:    self.next_direction = (0, -self.speed)
        if keys[pygame.K_DOWN]:  self.next_direction = (0, self.speed)

        # Перевірка можливості повороту
        old_pos = self.rect.copy()
        self.rect.x += self.next_direction[0]
        self.rect.y += self.next_direction[1]

        if self.rect.collidelist(walls) == -1:
            self.direction = self.next_direction
        
        self.rect = old_pos 

        # Постійний рух
        old_pos = self.rect.copy()
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        # Зупинка при зіткненні
        if self.rect.collidelist(walls) != -1:
            self.rect = old_pos
            # Пакмен не зупиняється назовсім, він чекає на нову команду або просто стоїть у стіні

    def draw(self, screen):
        screen.blit(self.image, self.rect)