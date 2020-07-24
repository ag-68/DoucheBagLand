import time
import pygame
import settings
import drawings
import inits
import routines


def run_game_stage_game_over(gainCoin, newBestScore, newLevel, score):
    fonts = pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[7])
    start_time = time.perf_counter()
    game_stage = "shop"
    GO_TEXTS = ["GAME OVER", "Your Score: " + str(int(score)), "New Best Score: " + str(int(inits.playerLog["BestScore"])), "New Level: " + settings.LEVEL_NAME[int(inits.playerLog["Level"])]]

    ii = -1
    complete = False
    while not complete:
        ii += 1
        run = True
        if ii == 1:
            if newBestScore:
                run = False
        if ii == 2:
            if not newBestScore:
                run = False
        if ii == 3:
            if not newLevel:
                run = False
        if ii > 5:
            run = False
            complete = True

        while run:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    complete = True
                    game_stage = "closing"

                # checking mouse clicks for updating sound buttons & sounds
                if event.type == inits.pygame.MOUSEBUTTONDOWN:
                    mx, my = inits.pygame.mouse.get_pos()
                    inits.SoundButtons.mouseAction(mx, my)
                    inits.exitGameButton.mouseAction(mx, my)

                # press enter to exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False

            if inits.exitGameButton.clicked:
                run = False
                complete = True
                game_stage = "closing"

            routines.sound_set_routine()

            disp_loc = (int(settings.WIN_DIM[0] / 2) - 100, int(settings.WIN_DIM[1] / 2))
            current_time = time.perf_counter()
            if current_time - start_time > settings.GAME_OVER_SCREEN_TIME:
                start_time = current_time
                run = False
            else:
                drawings.draw_all()
                if ii < 4:
                    game_over_text = fonts.render(GO_TEXTS[ii], 1, settings.GAME_OVER_COLOR)
                    inits.gameWindow.blit(game_over_text, disp_loc)
                elif ii == 4:
                    text1 = "Gained Coins: " + str(int(gainCoin))
                    text2 = "You Reached: " + str(int(inits.playerLog["Coins"])) + " Coins"
                    game_over_text = fonts.render(text1, 1, settings.GAME_OVER_COLOR)
                    inits.gameWindow.blit(game_over_text, (disp_loc[0], disp_loc[1]-20))
                    game_over_text = fonts.render(text2, 1, settings.GAME_OVER_COLOR)
                    inits.gameWindow.blit(game_over_text, (disp_loc[0], disp_loc[1] + 20))
                elif ii == 5:
                    text = settings.LEVEL_TEXT[inits.playerLog["Level"]].split(":")
                    max_len= max(len(text[0]), len(text[1]))
                    game_over_text = fonts.render(text[0], 1, settings.GAME_OVER_COLOR)
                    inits.gameWindow.blit(game_over_text, (disp_loc[0]+100-max_len/2*10, disp_loc[1]-20))
                    game_over_text = fonts.render(text[1], 1, settings.GAME_OVER_COLOR)
                    inits.gameWindow.blit(game_over_text, (disp_loc[0]+100-max_len/2*10, disp_loc[1] + 20))
                inits.gameDisp.update()

    return game_stage

