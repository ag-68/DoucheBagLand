import settings
import inits
import submodules
import routines
import drawings



def run_game_stage_name():

    game_stage = "connect"
    name = inits.nameButton.name
    gotName = False
    while gotName == False:

        inits.clock.tick(settings.SCREEN_UPDATE_CLOCK_TICK_INIT)

        # getting the new screen dimensions
        submodules.update_display_dimensions(inits.gameDisp)

        events = inits.pygame.event.get()
        for event in events:
            if event.type == inits.pygame.KEYDOWN:
                if len(name) < 10:
                    name += event.unicode
                if event.key == inits.pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == inits.pygame.K_RETURN:
                    gotName = True
                    game_stage = "play"
                    break
            elif event.type == inits.pygame.QUIT:
                gotName = True
                game_stage = "closing"
                break

            if event.type == inits.pygame.MOUSEBUTTONDOWN:
                mx, my = inits.pygame.mouse.get_pos()
                inits.SoundButtons.mouseAction(mx, my)
                #settings.connectButton.mouseAction(mx, my)
                inits.exitGameButton.mouseAction(mx, my)
                if inits.exitGameButton.clicked:
                    game_stage = "closing"
                    gotName = True

                if inits.playerLog["Coins"] > 0:
                    inits.goToShopButton.mouseAction(mx, my)
                    if inits.goToShopButton.clicked:
                        game_stage = "shop"
                        gotName = True



        # adjust the background and hit sounds
        routines.sound_set_routine()

        inits.nameButton.name = name
        inits.playerLog["Name"] = name
        drawings.draw_stage_name()
    return game_stage

