import settings
import inits

def sound_set_routine():

    # adjust the background and hit sounds
    if inits.SoundButtons.bg_sound == False:
        inits.game_sound_mixer.Channel(0).set_volume(0)
    elif inits.SoundButtons.bg_sound == True:
        inits.game_sound_mixer.Channel(0).set_volume(settings.BG_SOUND_LEVEL)

    if inits.SoundButtons.kick_sound == False:
        inits.game_sound_mixer.Channel(1).set_volume(0)
        inits.game_sound_mixer.Channel(2).set_volume(0)
        inits.game_sound_mixer.Channel(3).set_volume(0)
    elif inits.SoundButtons.kick_sound == True:
        inits.game_sound_mixer.Channel(1).set_volume(settings.HIT_SOUND_LEVEL)
        inits.game_sound_mixer.Channel(2).set_volume(settings.HIT_SOUND_LEVEL)
        inits.game_sound_mixer.Channel(3).set_volume(settings.HIT_SOUND_LEVEL)

def test_routine():
    count = 1
    rem = 0
    wait = True
    while wait:
        count += 1

        if count % 1000000 == 0:
            rem += 1
            print(str(rem) + " test test")
        if count % 10000000 == 0:
            wait = False