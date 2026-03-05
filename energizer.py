import pygame
import time

class Energizer:
    
    def __init__(self):
        self.active = False
        self.duration = 10  # секунд
        self.expiring_out_alert = 3 # секунд
        self.start_time = 0
        self.ghosts_eaten = 0
        
    def activate(self):
        self.active = True
        self.start_time = time.time()
        self.ghosts_eaten = 0
        
    def update(self):
        if self.active:
            elapsed = time.time() - self.start_time
            if elapsed >= self.duration:
                self.deactivate()
                
                
    def deactivate(self):
        self.active = False
        self.ghosts_eaten = 0
        
    def is_active(self):
        return self.active
    
    def get_next_ghost_score(self):
        score = 200 * (2 ** self.ghosts_eaten)
        if self.ghosts_eaten < 3:
            self.ghosts_eaten += 1
        return score
    
    def is_about_to_expire(self):
        if not self.active:
            return False
        return (self.duration - (time.time() - self.start_time)) <= self.expiring_out_alert