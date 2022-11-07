import pygame
import mytimer
from state import State

font = pygame.font.Font("./fonts/Square.ttf", 24)
main_font = pygame.font.Font("./fonts/ARCADE_N.ttf", 24)

class MainMenuState(State):

    def executeState(self):
        global main_font, font
        running = True
        
        picture = pygame.image.load("./media/font.png").convert_alpha()
        over_font = main_font.render("START", True, (255, 255, 255))
        end_font = main_font.render("QUIT", True, (255, 255, 255))
    
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
                        self.stateManager.ChangeState(MainGameState(timer))
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
            screen.fill((0,0,0))
            screen.blit(picture, (250,60))
            
            if status == False and menu_option == 1:
                screen.blit(over_font, (320,300))
            elif status == False and menu_option == 0:
                screen.blit(end_font, (320,400))
            else:
                screen.blit(over_font, (320,300))
                screen.blit(end_font, (320,400))
                    
            pygame.display.update()
            clock.tick(60)