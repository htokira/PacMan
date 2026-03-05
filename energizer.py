import pygame
import time

class Energizer:
    """
    Клас для керування станом енерджайзера.
    Відповідає за його таймер активності, стан вразливості привидів та підрахунок очок за з'їдання привидів.
    """
    
    def __init__(self):
        """
        Ініціалізує початкові параметри енерджайзера.
        """
        self.active = False
        self.duration = 10  # секунд
        self.expiring_out_alert = 3 # секунд
        self.start_time = 0
        self.ghosts_eaten = 0
        
    def activate(self):
        """
        Активує енерджайзер, скидаючи його таймер та кількість з'їдених привидів.
        """
        self.active = True
        self.start_time = time.time()
        self.ghosts_eaten = 0
        
    def update(self):
        """
        Оновлює стан об'єкта - перевіряє, чи не витрачено час активності.
        """
        if self.active:
            elapsed = time.time() - self.start_time
            if elapsed >= self.duration:
                self.deactivate()    
                
    def deactivate(self):
        """
        Вимикає енерджайзер та скидає кількість з'їдених привидів.
        """
        self.active = False
        self.ghosts_eaten = 0
        
    def is_active(self):
        """
        Перевіряє поточний статус активності енерджайзера.
        Returns:
            bool: True, якщо енерджайзер активний, інакше False.
        """
        return self.active
    
    def get_next_ghost_score(self):
        """
        Розраховує бали за наступного з'їденого привида за формулою $ 200 * 2^{n}$,
        де n — кількість з'їдених привидів.

        Returns:
            int: Кількість балів за привида.
        """
        score = 200 * (2 ** self.ghosts_eaten)
        if self.ghosts_eaten < 3:
            self.ghosts_eaten += 1
        return score
    
    def is_about_to_expire(self):
        """
        Перевіряє, чи залишилося часу активності менше, ніж встановлений поріг.
        Використовується для активації миготіння привидів.

        Returns:
            bool: True, якщо час дії майже закінчився, інакше False.
        """
        if not self.active:
            return False
        return (self.duration - (time.time() - self.start_time)) <= self.expiring_out_alert