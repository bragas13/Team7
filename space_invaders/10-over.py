import pygame
import math
import random
import mytimer
import sys
import time
from meteor import Meteor
from enemy import Enemy
from enemy import Extra_Enemy
from player import Player
from bullet import Bullet
from abc import ABC, abstractmethod

pygame.init()

invader_menu_pos = [(100,150), (100, 160), (100, 170), (100, 180), (100, 190), (100, 160), (100, 160)]

clock = pygame.time.Clock()
level = 1

# Game Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load("./media/stars.png")
background2 = pygame.transform.scale(pygame.image.load("./media/pngwing.com.png"), (800,600))

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

#extra enemies
extra_enemies_num = 2
extra_enemies = []

#meteors
num_meteors = 10
meteors = []

# Bullet
bullet = Bullet()

# Score Board
score_value = 0
font = pygame.font.Font("./fonts/Square.ttf", 24)
main_font = pygame.font.Font("./fonts/ARCADE_N.ttf", 24)
main_menu_font = pygame.font.Font("./fonts/invaders.ttf", 250)
invaders = pygame.font.Font("./fonts/invaders.ttf", 60)
textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font("./fonts/Square.ttf", 128) #create the font for game over

def randomize_enemies():
    global enemies
    enemies.clear()
    for i in range(num_enemies):
        enemies.append(Enemy())

def randomize_extra_enemy():
    global extra_enemies_num
    for i in range(extra_enemies_num):
        extra_enemies.append(Extra_Enemy())

def randomize_meteors():
    global meteors
    for i in range(num_meteors):
        meteors.append(Meteor())

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
    pygame.mixer.music.pause()
    screen.fill((0, 0, 0))
    over_font = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_font, (100, 250))

class State(ABC):
    
    def __init__(self, stateManager):
        self.stateManager = stateManager

    @abstractmethod
    def executeState(self):
        pass

class MainMenuState(State):
    def executeState(self):
        global score_value
        running = True
        
        invader = invaders.render("C", True, (0,100,50))
        menubackgr = pygame.transform.scale(pygame.image.load("./media/menubackgr.jpg"), (800,600))
        over_font = main_font.render("START", True, (255, 255, 255))
        end_font = main_font.render("QUIT", True, (255, 255, 255))
        title = main_menu_font.render("A", True, (255,255,255))
    
        menu_option = 0 # 0 for start, 1 for quit

        timer = mytimer.Timer(0.5)
        timer.start_timer()

        while running:
            for event in pygame.event.get():
                keystate = pygame.key.get_pressed()

                if keystate[pygame.K_DOWN]:
                    if menu_option == 0:
                        menu_option = 1
                        
                elif keystate[pygame.K_UP]:
                    if menu_option == 1:
                        menu_option = 0
                elif keystate[pygame.K_RETURN]:
                    if menu_option == 0:
                        mainPlayer.change_player_img( "./media/spaceship.png")
                        self.stateManager.ChangeState(MainGameState(timer))
                        score_value = 0
                        return
                    elif menu_option == 1:
                        timer.kill_thread()
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    timer.kill_thread()
                    pygame.quit()
                    sys.exit()

            status = timer.get_status()
            screen.blit(menubackgr,(0,0))
            screen.blit(title, (250,50))
            screen.blit(invader, (800,200))
            
            if status == False and menu_option == 1:
                screen.blit(over_font, (320,300))
            elif status == False and menu_option == 0:
                screen.blit(end_font, (320,400))
            else:
                screen.blit(over_font, (320,300))
                screen.blit(end_font, (320,400))
                    
            pygame.display.update()
            clock.tick(60)

class MainGameState(State):

    def __init__(self, timer):
        self.timer = timer

    def executeState(self):
        global mainPlayer, bullet, score_value, horizontalInput, enemies
        
        gameover = False
        t = 3
        
        randomize_enemies()
        
        # Game Loop
        running = True
        while running:
            if score_value > 1:
                self.stateManager.ChangeState(level2screen(self.timer))
                return
            if not gameover:
                # Game Events
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
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()

                # Screen Attributes
                screen.fill((0, 0, 0))
                screen.blit(background, (0, 0))

                mainPlayer.HandleMovement(horizontalInput)

                # Enemy Movement
                for i in range(num_enemies):
                    #Game Over
                    if enemies[i].y > 440: #trigger the end of the game
                        for j in range(num_enemies):
                            enemies[j].y = 2000
                        game_over()
                        gameover = True
                        break 
                        
                    
                    
                    enemies[i].mainGameMovement()

                    collision = isCollision(enemies[i].x, enemies[i].y, bullet.x, bullet.y) 
                    if collision:
                        explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                        explosion_sound.play()
                        bullet.bulletReady()
                        score_value += 1
                        enemies[i].MoveToRandomLocation()

                    genericBlit(enemies[i].x, enemies[i].y, enemies[i].img)

                if not gameover:
                    
                    # Bullet Animation
                    if bullet.y <= 0:
                        bullet.bulletReady()

                    if bullet.state is "fire": 
                        fire_bullet(bullet.x, bullet.y)
                        bullet.y -= bullet.y_change 

                    genericBlit(mainPlayer.x, mainPlayer.y, mainPlayer.img)
                    show_score(textX, textY)
            else:
                if(t <= 0):
                    running = False
                    self.stateManager.ChangeState(MainMenuState(self.timer))
                    return
                start = time.time()
                end = time.time()

                while(end - start == 0):
                    time.sleep(0.1)
                    end = time.time()
                    t -= end - start
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:          
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            clock.tick(60)

class level2screen(State):
    def __init__(self, timer):
        self.timer = timer

    def executeState(self):

        global score_value
       
        running = True
        message = main_font.render("LEVEL 2", True, (255, 255, 255))
        message2 = main_font.render("DODGE THE METEORS!", True, (255, 255, 255))
        message3 = main_font.render("END OF LEVEL BONUS: + 10 ", True, (50,255,50))
        pygame.mixer.music.pause()
        victory_sound = pygame.mixer.Sound("./media/mixkit-game-level-completed-2059.wav")
        victory_sound.play()
        score_value += 10

        while running:
            for event in pygame.event.get():
                keystate = pygame.key.get_pressed()

                if keystate[pygame.K_RETURN]:
                    self.stateManager.ChangeState(level2(self.timer))
                    return
                
                if event.type == pygame.QUIT:
                    self.timer.kill_thread()
                    pygame.quit()
                    sys.exit()
            
            screen.fill((0,0,0))
            screen.blit(message, (300,200))
            screen.blit(message2, (200,300))
            screen.blit(message3, (125,350))


            pygame.display.update()
            clock.tick(60)


        
class level2(State):
    def __init__(self, timer):
        self.timer = timer

    def executeState(self):
        global mainPlayer, score_value, horizontalInput, enemies, meteors, num_enemies
        
        gameover = False

        bullet.changeBulletImg("./media/laserBlue06.png")
        mainPlayer.change_player_img("./media/playerShip1_blue.png")
        num_enemies = 8

        pygame.mixer.music.load("./media/Ageispolis.wav")
        pygame.mixer.music.play(-1) 

        randomize_enemies()
        randomize_meteors()

        t = 3

        # Game Loop
        running = True
        while running:
            if score_value > 14:
                self.stateManager.ChangeState(level3screen(self.timer))
                return
            if not gameover:
                
                # Game Events
                for event in pygame.event.get():

                    horizontalInput = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                            horizontalInput = -1
                    if keystate[pygame.K_RIGHT]:
                            horizontalInput = 1
                    if keystate[pygame.K_SPACE]:
                        if bullet.state == "ready":
                                bullet_sound = pygame.mixer.Sound("./media/laser-gun-81720.wav")
                                bullet_sound.set_volume(0.5)
                                bullet_sound.play()
                                bullet.x = mainPlayer.x
                                fire_bullet(bullet.x, bullet.y)
                    if event.type == pygame.QUIT:
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()

                # Screen Attributes
                screen.fill((0, 0, 0))
                screen.blit(background2, (0, 0))

                mainPlayer.HandleMovement(horizontalInput)

                # Enemy Movement
                for i in range(num_enemies):
                    #Game Over
                    if enemies[i].y > 440: #trigger the end of the game
                        for j in range(num_enemies):
                            enemies[j].y = 2000
                        game_over()
                        gameover = True
                        break 
                        
                    enemies[i].mainGameMovement()

                    collision = isCollision(enemies[i].x, enemies[i].y, bullet.x, bullet.y) 
                    if collision:
                        explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                        explosion_sound.set_volume(0.75)
                        explosion_sound.play()
                        bullet.bulletReady()
                        score_value += 2
                        enemies[i].MoveToRandomLocation()

                    genericBlit(enemies[i].x, enemies[i].y, enemies[i].img)

                for i in range(num_meteors):
                    meteors[i].mainGameMovement()
                    collision = isCollision(meteors[i].x, meteors[i].y, mainPlayer.x, mainPlayer.y) 
                    if collision:
                        
                        explosion_sound = pygame.mixer.Sound("./media/deathsound.wav")
                        explosion_sound.play()
                        game_over()
                        gameover = True
                        break 
                    genericBlit(meteors[i].x, meteors[i].y, meteors[i].img)
                        
                if not gameover:
                    
                    # Bullet Animation
                    if bullet.y <= 0:
                        bullet.bulletReady()

                    if bullet.state is "fire": 
                        fire_bullet(bullet.x, bullet.y)
                        bullet.y -= bullet.y_change 

                    genericBlit(mainPlayer.x, mainPlayer.y, mainPlayer.img)
                    show_score(textX, textY)
            else:
                if(t <= 0):
                    running = False
                    self.stateManager.ChangeState(MainMenuState(self.timer))
                    break
                start = time.time()
                end = time.time()

                while(end - start == 0):
                    time.sleep(0.1)
                    end = time.time()
                    t -= end - start
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:          
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            clock.tick(60)

class level3screen(State):
    def __init__(self, timer):
        self.timer = timer

    def executeState(self):

        global score_value
       
        running = True
        message = main_font.render("Level3", True, (255, 255, 255))
        message2 = main_font.render("DONT DIE", True, (255, 255, 255))
        message3 = main_font.render("END OF LEVEL BONUS: + 20 ", True, (50,255,50))
        pygame.mixer.music.pause()
        victory_sound = pygame.mixer.Sound("./media/victory3.wav")
        victory_sound.play()
        score_value += 20

        while running:
            for event in pygame.event.get():
                keystate = pygame.key.get_pressed()

                if keystate[pygame.K_RETURN]:
                    self.stateManager.ChangeState(level3(self.timer))
                    return
                
                if event.type == pygame.QUIT:
                    self.timer.kill_thread()
                    pygame.quit()
                    sys.exit()
            
            screen.fill((0,0,0))
            screen.blit(message, (300,200))
            screen.blit(message2, (200,300))
            screen.blit(message3, (125,350))


            pygame.display.update()
            clock.tick(60)

        
class level3(State):
    def __init__(self, timer):
        self.timer = timer

    def executeState(self):
        global mainPlayer, score_value, horizontalInput, enemies, meteors, num_enemies,extra_enemies_nu
        
        gameover = False

        bullet.changeBulletImg("./media/laserBlue06.png")
        mainPlayer.change_player_img("./media/ship3.png")
        num_enemies = 12
       
        randomize_enemies()
        randomize_meteors()
        pygame.mixer.music.load("./media/bc3music.wav")
        pygame.mixer.music.play(-1) 

        t = 3

        # Game Loop
        running = True
        while running:
            if score_value > 40:
                self.stateManager.ChangeState(level4screen(self.timer))
                return
            if not gameover:
                
                # Game Events
                for event in pygame.event.get():

                    horizontalInput = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                            horizontalInput = -1
                    if keystate[pygame.K_RIGHT]:
                            horizontalInput = 1
                    if keystate[pygame.K_SPACE]:
                        if bullet.state == "ready":
                                bullet_sound = pygame.mixer.Sound("./media/gunshot.wav")
                                bullet_sound.set_volume(0.5)
                                bullet_sound.play()
                                bullet.x = mainPlayer.x
                                fire_bullet(bullet.x, bullet.y)
                    if event.type == pygame.QUIT:
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()

                # Screen Attributes
                screen.fill((0, 0, 0))
                screen.blit(background2, (0, 0))

                mainPlayer.HandleMovement(horizontalInput)

                # Enemy Movement
                for i in range(num_enemies):
                    #Game Over
                    if enemies[i].y > 440: #trigger the end of the game
                        for j in range(num_enemies):
                            enemies[j].y = 2000
                        game_over()
                        gameover = True
                        break 
                        
                    enemies[i].mainGameMovement()

                    collision = isCollision(enemies[i].x, enemies[i].y, bullet.x, bullet.y) 
                    if collision:
                        explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                        explosion_sound.set_volume(0.75)
                        explosion_sound.play()
                        bullet.bulletReady()
                        score_value += 2
                        enemies[i].MoveToRandomLocation()

                    genericBlit(enemies[i].x, enemies[i].y, enemies[i].img)

                for i in range(num_meteors):
                    meteors[i].mainGameMovement()
                    collision = isCollision(meteors[i].x, meteors[i].y, mainPlayer.x, mainPlayer.y) 
                    if collision:
                        
                        explosion_sound = pygame.mixer.Sound("./media/deathsound.wav")
                        explosion_sound.play()
                        game_over()
                        gameover = True
                        break 
                    genericBlit(meteors[i].x, meteors[i].y, meteors[i].img)
                        
                if not gameover:
                    
                    # Bullet Animation
                    if bullet.y <= 0:
                        bullet.bulletReady()

                    if bullet.state is "fire": 
                        fire_bullet(bullet.x, bullet.y)
                        bullet.y -= bullet.y_change 

                    genericBlit(mainPlayer.x, mainPlayer.y, mainPlayer.img)
                    show_score(textX, textY)
            else:
                if(t <= 0):
                    running = False
                    self.stateManager.ChangeState(MainMenuState(self.timer))
                    break
                start = time.time()
                end = time.time()

                while(end - start == 0):
                    time.sleep(0.1)
                    end = time.time()
                    t -= end - start
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:          
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            clock.tick(60)

class level4screen(State):
    def __init__(self, timer):
        self.timer = timer

    def executeState(self):

        global score_value
       
        running = True
        message = main_font.render("Level4", True, (255, 255, 255))
        message2 = main_font.render("Extra Enemies Extra points", True, (255, 255, 255))
        message3 = main_font.render("END OF LEVEL BONUS: + 30 ", True, (50,255,50))
        pygame.mixer.music.pause()
        victory_sound = pygame.mixer.Sound("./media/victory3.wav")
        victory_sound.play()
        score_value += 30

        while running:
            for event in pygame.event.get():
                keystate = pygame.key.get_pressed()

                if keystate[pygame.K_RETURN]:
                    self.stateManager.ChangeState(level4(self.timer))
                    return
                
                if event.type == pygame.QUIT:
                    self.timer.kill_thread()
                    pygame.quit()
                    sys.exit()
            
            screen.fill((0,0,0))
            screen.blit(message, (300,200))
            screen.blit(message2, (200,300))
            screen.blit(message3, (125,350))


            pygame.display.update()
            clock.tick(60)

class level4(State):
    def __init__(self, timer):
        self.timer = timer

    def executeState(self):
        global mainPlayer, score_value, horizontalInput, enemies, meteors, num_enemies, extra_enemies_num
        
        gameover = False

        randomize_enemies()
        randomize_meteors()
        randomize_extra_enemy()

        bullet.changeBulletImg("./media/bullet4.png")
        mainPlayer.change_player_img("./media/ship4.png")
        num_enemies = 12
        extra_enemies_num = 2

        pygame.mixer.music.load("./media/bc4music.wav")
        pygame.mixer.music.play(-1) 

        t = 3

        # Game Loop
        running = True
        while running:
            if not gameover:
                
                # Game Events
                for event in pygame.event.get():

                    horizontalInput = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                            horizontalInput = -1
                    if keystate[pygame.K_RIGHT]:
                            horizontalInput = 1
                    if keystate[pygame.K_SPACE]:
                        if bullet.state == "ready":
                                bullet_sound = pygame.mixer.Sound("./media/gunshot.wav")
                                bullet_sound.set_volume(0.5)
                                bullet_sound.play()
                                bullet.x = mainPlayer.x
                                fire_bullet(bullet.x, bullet.y)
                    if event.type == pygame.QUIT:
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()

                # Screen Attributes
                screen.fill((0, 0, 0))
                screen.blit(background2, (0, 0))

                mainPlayer.HandleMovement(horizontalInput)

                # Enemy Movement
                for i in range(num_enemies):
                    #Game Over
                    if enemies[i].y > 440: #trigger the end of the game
                        for j in range(num_enemies):
                            enemies[j].y = 2000
                        game_over()
                        gameover = True
                        break 
                        
                    enemies[i].mainGameMovement()

                    collision = isCollision(enemies[i].x, enemies[i].y, bullet.x, bullet.y) 
                    if collision:
                        explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                        explosion_sound.set_volume(0.75)
                        explosion_sound.play()
                        bullet.bulletReady()
                        score_value += 2
                        enemies[i].MoveToRandomLocation()

                    genericBlit(enemies[i].x, enemies[i].y, enemies[i].img)

                for i in range(extra_enemies_num):
                    if extra_enemies[i].y > 440:
                        for j in range(extra_enemies_num):
                            extra_enemies[j].y = 2000

                        game_over()
                        gameover = True
                        break

                    extra_enemies[i].mainGameMovement()

                    collision = isCollision(extra_enemies[i].x, extra_enemies[i].y, bullet.x, bullet.y)
                    if collision:
                        explosion_sound = pygame.mixer.Sound("./media/explosion.wav")
                        explosion_sound.set_volume(0.75)
                        explosion_sound.play()
                        bullet.bulletReady()
                        score_value += 4
                        extra_enemies[i].MoveToRandomLocation()

                    genericBlit(extra_enemies[i].x, extra_enemies[i].y, extra_enemies[i].img)


                for i in range(num_meteors):
                    meteors[i].mainGameMovement()
                    collision = isCollision(meteors[i].x, meteors[i].y, mainPlayer.x, mainPlayer.y) 
                    if collision:
                        
                        explosion_sound = pygame.mixer.Sound("./media/deathsound.wav")
                        explosion_sound.play()
                        game_over()
                        gameover = True
                        break 
                    genericBlit(meteors[i].x, meteors[i].y, meteors[i].img)
                        
                if not gameover:
                    
                    # Bullet Animation
                    if bullet.y <= 0:
                        bullet.bulletReady()

                    if bullet.state is "fire": 
                        fire_bullet(bullet.x, bullet.y)
                        bullet.y -= bullet.y_change 

                    genericBlit(mainPlayer.x, mainPlayer.y, mainPlayer.img)
                    show_score(textX, textY)
            else:
                if(t <= 0):
                    running = False
                    self.stateManager.ChangeState(MainMenuState(self.timer))
                    break
                start = time.time()
                end = time.time()

                while(end - start == 0):
                    time.sleep(0.1)
                    end = time.time()
                    t -= end - start
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:          
                        self.timer.kill_thread()
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            clock.tick(60)


class GameState():
    def __init__(self):
        self.state = MainMenuState(self)
    
    def executeState(self):
        self.state.executeState()

    def ChangeState(self, newState):
        print("Chanign state to", newState)
        self.state = newState 
        newState.stateManager = self


game_state = GameState()
# Game Loop
running = True
while running:
    # Game Events
    game_state.executeState()
    print(game_state.state)
    clock.tick(60)

