import pygame


class Player():

    def __init__(self):
        self.img = pygame.image.load("./media/spaceship.png")
        
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.changeMultiplier = 3
        

    def HandleMovement(self, horizontalInput):
        self.x += horizontalInput * self.changeMultiplier
    
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736