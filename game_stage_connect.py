import pygame
import settings
import drawings
import submodules


def run_game_stage_connect():


    settings.connectButton.reset()
    # Initial Phase before connecting to server
    while settings.playerReady == False:

        # getting the new screen dimensions
        submodules.update_display_dimensions(pygame.display)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                settings.playerReady = True
                game_stage = "closing"
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                settings.SoundButtons.mouseAction(mx, my)
                settings.connectButton.mouseAction(mx, my)
                settings.exitGameButton.mouseAction(mx, my)
                if settings.exitGameButton.clicked:
                    game_stage = "closing"
                    settings.playerReady = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    settings.connectButton.clicked = True
                    settings.connectButton.text = "Connecting to Server..."
                    settings.connectButton.font = 30

        if settings.connectButton.clicked == True:
            settings.playerReady = True
            game_stage = "play"

        # adjust the background and hit sounds
        if settings.SoundButtons.bg_sound == False:
            settings.game_sound_mixer.Channel(0).set_volume(0)
        elif settings.SoundButtons.bg_sound == True:
            settings.game_sound_mixer.Channel(0).set_volume(settings.BG_SOUND_LEVEL)

        if settings.SoundButtons.kick_sound == False:
            settings.game_sound_mixer.Channel(1).set_volume(0)
            settings.game_sound_mixer.Channel(2).set_volume(0)
        elif settings.SoundButtons.kick_sound == True:
            settings.game_sound_mixer.Channel(1).set_volume(settings.HIT_SOUND_LEVEL)
            settings.game_sound_mixer.Channel(2).set_volume(settings.HIT_SOUND_LEVEL)

        # update the display window
        drawings.draw_stage_connect()

        # wait time
        settings.clock.tick(settings.SCREEN_UPDATE_CLOCK_TICK_INIT)

    settings.playerReady = False
    settings.connectButton.clicked = False
    return game_stage
