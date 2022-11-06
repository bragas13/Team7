import pygame

class Bullet():

    def __init__(self):
        self.Img = pygame.image.load("./media/bullet.png")
        self.x = 0
        self.y = 480
        self.x_change = 0
        self.y_change = 10
        self.state = "ready"

    
    def bulletReady(self):
        self.state = "ready"
        self.y = 480