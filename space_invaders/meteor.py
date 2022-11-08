import pygame
import math
import random


class Meteor():
    def __init__(self):
        self.img = pygame.transform.scale((pygame.image.load("./media/meteorGrey_big1.png")), (40,40))
        self.x = (random.randint(2, 735))
        self.y = (random.randint(-100, -40))
        self.x_change = (random.randint(-3,3))
        self.y_change = (random.randint(2,4))

    def mainGameMovement(self):          
        self.x += self.x_change
        self.y += self.y_change
        if self.x < -25 or self.x > 850 or self.y > 650:
            self.x = (random.randint(30, 735))
            self.y = (random.randint(-100, -40))
            self.x_change = (random.randint(-6,6))
            self.y_change = (random.randint(1,3))
