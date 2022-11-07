import pygame


class Player():

    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load("./media/spaceship.png"), (80,50))
        
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.changeMultiplier = 4
    
    def change_player_img(self,img):
        self.img = pygame.transform.scale(pygame.image.load(img), (80,50))

    def HandleMovement(self, horizontalInput):
        self.x += horizontalInput * self.changeMultiplier
    
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736