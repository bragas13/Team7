import pygame
import random
import sys
import time
from powerups_type import PowerUp
import threading


# GLOBAL VARIABLES
double_click_event = pygame.USEREVENT + 1
timer = 0
time_to_powerup = 0.30
powerup_on_field = False
powerup_type = PowerUp.BIG_PADDEL
powerup_activated = False
powerup_for_player = False

powerup_run_time = 10

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200, 200, 200)
black = (0,0,0)
bg_color = pygame.Color('grey12')
powerup_color = (0,0,0)

# Images
powerup_image = pygame.image.load('./assets/powerup.jpg')
powerup_image = pygame.transform.scale(powerup_image, (80,80))
ball_image = pygame.image.load('./assets/ball.png')
background_image = pygame.image.load('./assets/background.jpg')
background_image = pygame.transform.scale(background_image, (1280,800))
background_rect = background_image.get_rect()

# Game Rectangle
ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
player = pygame.Rect(screen_width-20, screen_height/ \
                     2-70, 10, 140)  # -70 missing

opponent = pygame.Rect(10, screen_height/2-70, 10, 140)  # -70 missing
powerup = pygame.Rect(screen_width/2-15, screen_height/2-15, 80, 80)


# Game Variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 3

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# Sound Variables
pong_sound = pygame.mixer.Sound("./media/cartoon-jump-6462.wav")
score_sound = pygame.mixer.Sound("./media/correct-2-46134.wav")



# FUNCTIONS

def powerup_time():
  global powerup_run_time
  while powerup_run_time > 0:
    start = time.time()
    time.sleep(0.1)
    end = time.time()
    powerup_run_time -= (end - start)

def create_powerup():
  global time_to_powerup, powerup_on_field, powerup_color, powerup_for_player, powerup_activated,powerup_type

  powerup.x = random.randint(100,700)
  powerup.y = random.randint(100,500)
  powerup_on_field = True
  time_to_powerup = 0.50
  powerup_color = (random.randint(5,240),random.randint(5,240),random.randint(5,240))
  powerup_num = random.randint(1,3)
  powerup_type = PowerUp(powerup_num)

def ball_animation():

  global ball_speed_x, ball_speed_y, player_score, opponent_score, powerup_on_field, powerup_activated, powerup_for_player, player,opponent,powerup_type

  ball.x += ball_speed_x
  ball.y += ball_speed_y

  # Ball Collision
  if ball.top <= 0 or ball.bottom >= screen_height:
    ball_speed_y *= -1

  # Ball Collision Left
  if ball.left <= 0:
    pygame.mixer.Sound.play(score_sound)
    player_score += 1
    ball_restart()

  # Ball Collision Right
  if ball.right >= screen_width:
    pygame.mixer.Sound.play(score_sound)
    opponent_score += 1
    ball_restart()


  # Ball Collision (Player)
  if ball.colliderect(player): 
    pygame.mixer.Sound.play(pong_sound)
    if((player_speed < 0) and (ball_speed_y > 0)) or ((player_speed > 0) and (ball_speed_y < 0)):
      ball_speed_x *=-1
      ball_speed_y *=-1
    else:
      ball_speed_x *= -1

  if ball.colliderect(opponent):
    pygame.mixer.Sound.play(pong_sound)
    ball_speed_x *= -1

  if powerup_on_field == True:
    if ball.colliderect(powerup):
      if ball_speed_x < 0:
        powerup_for_player = True
      elif ball_speed_x > 0:
        powerup_for_player = False

      powerup_activated = True
      powerup_on_field = False
      
      if powerup_type == PowerUp.BIG_PADDEL:
        if ball_speed_x > 0:
          opponent = opponent = pygame.Rect(10, screen_height/2-70, 10, 500)
        else:
          player = pygame.Rect(screen_width-20, screen_height/ \
                     2-70, 10, 500)
      
      elif powerup_type == PowerUp.SMALL_OPPONENT:
        if ball_speed_x > 0:
          player = pygame.Rect(screen_width-20, screen_height/ \
                     2-70, 10, 50)
        else:
          opponent = pygame.Rect(10, screen_height/2-70, 10, 50)
      else:
        ball_speed_x = ball_speed_x * 2
        ball_speed_y = ball_speed_y * 2

      x = threading.Thread(target=powerup_time)
      x.start()


def player_animation():

  global player_speed

  player.y += player_speed

  # Player Collision
  if player.top <= 0:
    player.top = 0

  if player.bottom >= screen_height:
    player.bottom = screen_height


def opponent_ai():
  
  global opponent_speed

  if opponent.top < ball.top : #opponent is above ball
    opponent.y += opponent_speed

  if opponent.bottom > ball.bottom: # opponent is below ball
    opponent.y -= opponent_speed

  if opponent.top <= 0:
    opponent.top = 0

  if opponent.bottom >= screen_height:
    opponent.bottom = screen_height
#Mod for speeding up ai the more you score
  if player_score > 6:
      opponent_speed = 5
  if player_score > 10:
      opponent_speed = 7 

  
def ball_restart():
  
  global ball_speed_x, ball_speed_y

  ball.center = (screen_width/2, screen_height/2)

  ball_speed_y *= random.choice((1, -1)) 
  ball_speed_x *= random.choice((1, -1)) 

#Add score limit of 12 
def game_restart():
  global player_score, opponent_score, opponent_speed
  opponent_speed = 3
  player_score =0
  opponent_score = 0

  ball_restart()
  #This will check the pygame event if the arrow key up is double clicked within a timer
def check_double_click_up():
  global timer, player_speed

  if timer == 0:
    timerset = True
  else:
    if timer == 1:
       player.y -= 100
       timerset = False
  
  if timerset:
    timer = 1
    return
  else:
    timer = 0
    return
#This will check the pygame event if the arrow key down is double clicked within a timer
def check_double_click_down():

  global timer, player_speed

  if timer == 0:
    timerset = True
  else:
    if timer == 1:
       player.y += 100
       timerset = False
  
  if timerset:
    timer = 1
    return
  else:
    timer = 0
    return

if __name__ == "__main__":

  # GAME LOOP
  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          
          if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
              check_double_click_up()
              player_speed -= 6
            if event.key == pygame.K_DOWN:
              player_speed += 6
              check_double_click_down()

          if event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
              player_speed += 6
            if event.key == pygame.K_DOWN:
              player_speed -= 6

      if powerup_activated == True and powerup_run_time <= 0:
        opponent = pygame.Rect(opponent.x, opponent.y, 10, 140)
        player = pygame.Rect(player.x, player.y, 10, 140)
        time_to_powerup = 0.30
        powerup_on_field = False

        if powerup_type == PowerUp.FAST_BALL:
          ball_speed_y = ball_speed_y / 2
          ball_speed_x = ball_speed_x / 2

        powerup_type = PowerUp.BIG_PADDEL
        powerup_activated = False
        powerup_for_player = False
        powerup_run_time = 10
      

      ball_animation()
      player_animation()
      opponent_ai()

      screen.blit(background_image, background_rect)
      pygame.draw.rect(screen, light_grey, player)
      pygame.draw.rect(screen, light_grey, opponent)
      screen.blit(ball_image, ball)

      pygame.draw.aaline(screen, light_grey, (screen_width/2,
                                              0), (screen_width/2, screen_height))


      if player_score == 12 or opponent_score == 12:
        game_restart()
      
      
      if powerup_on_field == False and powerup_activated == False:
        start = time.time()
        end = time.time()

        while ((end - start) == 0):
          end = time.time()

        time_to_powerup -= (end - start)
        
        if time_to_powerup <= 0:
          create_powerup()
      
      elif powerup_on_field == True and powerup_activated == False:
        #pygame.draw.rect(screen, powerup_color, powerup)
        screen.blit(powerup_image, (powerup.x ,powerup.y))
        start = time.time()
        end = time.time()

        while ((end - start) == 0):
          end = time.time()

        time_to_powerup -= (end - start)
        
        if time_to_powerup <= 0:
          powerup_on_field = False
          time_to_powerup = 0.30

      # Create a surface for the scores
      player_text = basic_font.render(f"{player_score}", False, light_grey)
      screen.blit(player_text, (660,470))

      opponent_text = basic_font.render(f"{opponent_score}", False, light_grey)
      screen.blit(opponent_text, (600,470))

      if powerup_activated == True:
        power_up_text = basic_font.render(f"PowerUp Time: {round(powerup_run_time,1)}", False, light_grey)
        screen.blit(power_up_text, (200,200))


      



      pygame.display.flip()
      clock.tick(60)

