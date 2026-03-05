import pygame
import time

class Energizer:
    
    def __init__(self):
        self.active = False
        self.duration = 10  # секунд
        self.start_time = 0
        
    def activate(self):
        self.active = True
        print("Активовано")
        self.start_time = time.time()
        
    def update(self):
        if self.active:
            elapsed = time.time() - self.start_time
            if elapsed >= self.duration:
                self.deactivate()
                
    def deactivate(self):
        self.active = False
        print("Деактивано") #temp
        
    def is_active(self):
        return self.active