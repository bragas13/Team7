import pygame
import random
import sys
import score_text
<<<<<<< HEAD
import variables
import sound
=======
from variables import *
<<<<<<< HEAD
>>>>>>> 25a2c179261283dd97f1f4bf5991249de7c0093d
=======
from colors import *
>>>>>>> 555bd8de3b38c26a77ba8519d79293ca6435cf42

# GLOBAL VARIABLES

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')


# Game Rectangle
ball = pygame.Rect(screen_width/2-15, screen_height/2-15, 30, 30)
player = pygame.Rect(screen_width-20, screen_height/ \
                     2-70, 10, 140)  # -70 missing
opponent = pygame.Rect(10, screen_height/2-70, 10, 140)  # -70 missing

player_score, opponent_score, basic_font = score_text.setup_score()

<<<<<<< HEAD
pong_sound, score_sound = sound.innit_sound()
=======
# Sound Variables
<<<<<<< HEAD
#pong_sound = pygame.mixer.Sound("./media/pong.ogg")
#score_sound = pygame.mixer.Sound("./media/score.ogg")
>>>>>>> 25a2c179261283dd97f1f4bf5991249de7c0093d
=======
pong_sound = pygame.mixer.Sound("./media/pong.ogg")
score_sound = pygame.mixer.Sound("./media/score.ogg")
>>>>>>> 555bd8de3b38c26a77ba8519d79293ca6435cf42

# FUNCTIONS

def ball_animation():

  global ball_speed_x, ball_speed_y, player_score, opponent_score

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
  if ball.colliderect(player) or ball.colliderect(opponent):
    pygame.mixer.Sound.play(pong_sound)
    ball_speed_x *= -1


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

  
def ball_restart():
  
  global ball_speed_x, ball_speed_y

  ball.center = (screen_width/2, screen_height/2)

  ball_speed_y *= random.choice((1, -1)) 
  ball_speed_x *= random.choice((1, -1)) 




if __name__ == "__main__":

  # GAME LOOP
  while True:

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
              player_speed -= 6
            if event.key == pygame.K_DOWN:
              player_speed += 6
          if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
              player_speed += 6
            if event.key == pygame.K_DOWN:
              player_speed -= 6

      ball_animation()
      player_animation()
      opponent_ai()

      screen.fill(bg_color)
      pygame.draw.rect(screen, light_grey, player)
      pygame.draw.rect(screen, light_grey, opponent)
      pygame.draw.ellipse(screen, light_grey, ball)
      pygame.draw.aaline(screen, light_grey, (screen_width/2,
                                              0), (screen_width/2, screen_height))


      # Create a surface for the scores
      player_text = basic_font.render(f"{player_score}", False, light_grey)
      screen.blit(player_text, (660,470))

      opponent_text = basic_font.render(f"{opponent_score}", False, light_grey)
      screen.blit(opponent_text, (600,470))


      pygame.display.flip()
      clock.tick(60)

