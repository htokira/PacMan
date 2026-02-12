import pygame
import math
import copy

class Map:
    def __init__(self, screen, level_data, width, height):
        self.screen = screen
        self.level = copy.deepcopy(level_data)
        self.width = width
        self.height = height

        self.rows = len(self.level)
        self.cols = len(self.level[0])
        self.h = (self.height - 50) // self.rows
        self.w = self.width // self.cols

    def draw_map(self):
        PI = math.pi

        for i in range(self.rows):
            for j in range(self.cols):
                val = self.level[i][j]
                center_x = int(j * self.w + (0.5 * self.w))
                center_y = int(i * self.h + (0.5 * self.h))
                
                if val == 1:
                    pygame.draw.circle(self.screen, 'white', (center_x, center_y), 4)
                elif val == 2:
                    pygame.draw.circle(self.screen, 'white', (center_x, center_y), 10)
                elif val == 3:
                    pygame.draw.line(self.screen, 'blue', (center_x, i * self.h), (center_x, i * self.h + self.h), 3) #замінити колір для інших рівнів
                elif val == 4:
                    pygame.draw.line(self.screen, 'blue', (j * self.w, center_y), (j * self.w + self.w, center_y), 3)
                elif val == 5:
                    pygame.draw.arc(self.screen, 'blue', [(j * self.w - (self.w * 0.5)), (i * self.h + (0.5 * self.h)), self.w, self.h], 0, PI/2, 3)
                elif val == 6:
                    pygame.draw.arc(self.screen, 'blue', [(j * self.w + (self.w * 0.5)), (i * self.h + (0.5 * self.h)), self.w, self.h], PI/2, PI, 3)
                elif val == 7:
                    pygame.draw.arc(self.screen, 'blue', [(j * self.w + (self.w * 0.5)), (i * self.h - (0.5 * self.h)), self.w, self.h], PI, 3*PI/2, 3)
                elif val == 8:
                    pygame.draw.arc(self.screen, 'blue', [(j * self.w - (self.w * 0.5)), (i * self.h - (0.5 * self.h)), self.w, self.h], 3*PI/2, 2*PI, 3)
                elif val == 9:
                    pygame.draw.line(self.screen, 'white', (j * self.w, center_y), (j * self.w + self.w, center_y), 3)

    #Перевірка чи гравець може йти, викликати перед рухом у методі гравця
    def can_move(self, x, y):
        col = int(x // self.w)
        row = int(y // self.h)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.level[row][col] <= 2:
                return True
            
        return False
    
    #Перевірка з яким об'єктом стикнувся гравець, викликати після руха гравця
    def collision_with_objects(self, x, y):
        score = 0
        col = int(x // self.w)
        row = int(y // self.h)

        if 0 <= row < self.rows and 0 <= col < self.cols:
            position = self.level[row][col]

            if position == 1:
                score = 1
                self.level[row][col] = 0
            elif position == 2:
                score = 50
                self.level[row][col] = 0
                # логіка енерджайзера

        return score