import pygame
import time
import settings
import inits

def run_game_stage_welcome():
    # the next stage unless quit
    game_stage = "name"

    curr_time = time.perf_counter()
    ii = -1
    quitAll = False
    while ii < len(settings.WELCOME_TEXT)-1 and not quitAll:
        ii += 1
        text = settings.WELCOME_TEXT[ii]
        ll = -1
        while ll < len(text) and not quitAll:
            ll += 1
            wait = True
            while wait:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        wait = False
                        quitAll = True
                        game_stage = "closing"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            wait = False
                            quitAll = True
                            game_stage = "name"

                if time.perf_counter() - curr_time > 0.15:
                    curr_time = time.perf_counter()
                    wait = False
            font = pygame.font.SysFont(settings.DISP_FONT, 30)
            display_text = font.render(text[0:ll], 1, settings.WELCOME_TEXT_COLOR)
            inits.gameWindow.blit(display_text, (int(settings.WIN_DIM[0] / 2) - 100,
                                                    int(settings.WIN_DIM[1] / 2) - 100 + ii * 30))
            pygame.display.update()


    return game_stage