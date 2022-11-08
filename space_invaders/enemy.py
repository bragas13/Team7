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
        self.y_change = 30

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

class Harder_Enemy():
    def __init__(self):
        print("starting enemy")
        self.img = pygame.transform.scale(pygame.image.load("./media/enemyRed5.png"), (80,40))
        self.x = (random.randint(2, 735))
        self.y = (random.randint(-200, 0))
        self.x_change = (random.randint(-4,4))
        self.y_change = 1

    def mainGameMovement(self):          
        self.x += self.x_change
        self.y += self.y_change
        if self.x <= 0:
            self.x_change = self.x_change * -1
        elif self.x >= 736:
            self.x_change = self.x_change * -1
    
    def MoveToRandomLocation(self):
        self.x = random.randint(2, 736) 
        self.y = random.randint(-200, 0)



class Extra_Enemy():

    def __init__(self):
        print("starting enemy")
        self.img = pygame.transform.scale(pygame.image.load("./media/enemyBlack1.png"), (80,80))
        self.x = (random.randint(2, 735))
        self.y = (random.randint(-1000, -500))
        self.x_change = 2
        self.y_change = (random.randint(3,5))

    def mainGameMovement(self,player_x):
      
        self.y += self.y_change
        if self.x < player_x:
            self.x += self.x_change
        if self.x > player_x:
            self.x -= self.x_change
        if self.y > 1000:
            self.MoveToRandomLocation()

    def MoveToRandomLocation(self):
        self.x = random.randint(2, 736) 
        self.y = random.randint(-1000, -500)
        
    def GetExtraEnemyX(self):
        return self.x
    def GetExtraEnemyY(self):
        return self.y
    
    def GetExtraEnemyImg(self):
        return self.img