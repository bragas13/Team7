import pygame
import math
import random
import time
from enemy import Enemy
from player import Player
from bullet import Bullet

pygame.init()
clock = pygame.time.Clock()
level = 1

# Game Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load("./media/stars.png")

# Sound
pygame.mixer.music.load("./media/background.wav")
pygame.mixer.music.play(-1) 
explosion_sound = pygame.mixer.Sound("./media/explosion.wav")

# Player
horizontalInput = 0
mainPlayer = Player()


# Enemy
num_enemies = 6
enemies = []

for i in range(num_enemies):
    enemies.append(Enemy())

# Bullet
bullet = Bullet()

# Score Board
score_value = 0
font = pygame.font.Font("./fonts/Square.ttf", 24)
textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font("./fonts/Square.ttf", 128) #create the font for game over

def show_score(x, y):
    score = font.render("Score: "+str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def genericBlit(x,y, img):
    screen.blit(img, (x,y))

def fire_bullet(x, y):
    global bullet

    bullet.state = "fire"
    genericBlit(x+16, y+10, bullet.Img)


#returns the magnitude of a vector between the enemy and the bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):

    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
                                           
    if distance < 27:
        return True
    else:
        return False

def game_over(): # display the game over text
    over_font = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_font, (100, 250))

class GameState():
    def __init__(self):
        self.state = 'main_game'
    
    #todo: 
    # def intro
    # def game_over_screen
    # def level 2 and 3

    def main_game(self):
        global horizontalInput, bullet , score_value, mainPlayer
        
        for event in pygame.event.get():

            horizontalInput = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                    horizontalInput = -1
            if keystate[pygame.K_RIGHT]:
                    horizontalInput = 1
            if keystate[pygame.K_SPACE]:
                if bullet.state == "ready":
                        bullet_sound = pygame.mixer.Sound("./media/laser.wav")
                        bullet_sound.play()
                        bullet.x = mainPlayer.x
                        fire_bullet(bullet.x, bullet.y)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                    

        # Screen Attributes
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Player Movement
        mainPlayer.HandleMovement(horizontalInput)

        # Enemy Movement
        for i in range(num_enemies):

            # #Game Over
            if enemies[i].y > 440: #trigger the end of the game
                for j in range(num_enemies):
                    enemies[j].y = 2000
                game_over()
                break 
            

            collision = isCollision(enemies[i].x, enemies[i].y, bullet.x, bullet.y) 
            if collision:
                explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                explosion_sound.play()
                bullet.bulletReady()
                score_value += 1
                enemies[i].MoveToRandomLocation()

            enemies[i].mainGameMovement()

            genericBlit(enemies[i].x, enemies[i].y, enemies[i].img)

        # Bullet Animation
        if bullet.y <= 0: 
            bullet.bulletReady()

        if bullet.state == "fire": 
            fire_bullet(bullet.x, bullet.y)
            bullet.y -= bullet.y_change 

        genericBlit(mainPlayer.x, mainPlayer.y, mainPlayer.img)
        show_score(textX, textY)

        pygame.display.update()

game_state = GameState()
# Game Loop
running = True
while running:
    # Game Events
    game_state.main_game()
    clock.tick(60)