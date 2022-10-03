import pygame

def innit_sound():
    pong_sound = pygame.mixer.Sound("./media/pong.ogg")
    score_sound = pygame.mixer.Sound("./media/score.ogg")
    
    return pong_sound, score_sound