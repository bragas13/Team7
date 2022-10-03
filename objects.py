import pygame

def draw_objects(screen, light_grey, player, opponent, ball, screen_width, screen_height):
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2,
                                              0), (screen_width/2, screen_height))