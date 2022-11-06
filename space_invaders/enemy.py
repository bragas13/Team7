import pygame
import math
import random

class Enemy():

    def __init__(self):
        print("starting enemy")
        self.img = (pygame.image.load("./media/ufo.png"))
        self.x = (random.randint(2, 735))
        self.y = (random.randint(50, 150))
        self.x_change = (random.randint(2,6))
        self.y_change = (random.randint(30,50))

    def mainGameMovement(self):          
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 4
            self.y += self.y_change
        elif self.x >= 736:
            self.x = -4
            self.y += self.y_change

    def MoveToRandomLocation(self):
        self.x = random.randint(2, 736) 
        self.y = random.randint(50, 150)
        
    def GetEnemyX(self):
        return self.x
    def GetEnemyY(self):
        return self.y
    
    def GetEnemyImg(self):
        return self.img
