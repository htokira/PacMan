import pygame
from map import Map
from levels import LEVEL1

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
activeLevel = LEVEL1

game_map = Map(screen, activeLevel, WIDTH, HEIGHT)

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    game_map.draw_map()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()