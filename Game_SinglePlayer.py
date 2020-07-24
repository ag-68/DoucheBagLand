"""
The classic game of flappy bird. Make with python
and pygame. Features pixel perfect collision using masks :o

Date Modified:  Jul 30, 2019
Author: Tech With Tim
Estimated Work Time: 5 hours (1 just for that damn collision)
"""
import pygame
import os
from player import Player
from soundbutton import SoundButton


pygame.font.init()  # init font
pygame.init()

# WINDOW & IMAGE DIMENSIONS
WIN_WIDTH = 900
WIN_HEIGTH = 600
FRAME_WIDTH=50
FRAMED_WIN_DIMENSIONS = [WIN_WIDTH, WIN_HEIGTH, FRAME_WIDTH]
FRAME_COLOR=(10,80,130)
PLAYER_ICON_WIDTH=50
PUNCH_ICON_WIDTH=30 #int(PLAYER_ICON_WIDTH/2.2)
PUNCH_ICON_HEIGTH=30 #PUNCH_ICON_WIDTH
KICK_ICON_WIDTH=68 #int(PLAYER_ICON_WIDTH/1.5)
KICK_ICON_HEIGTH=41 #PUNCH_ICON_HEIGTH
VOLUME_BUTTON_WIDTH=30
ICON_DIMENSIONS=[]
ICON_DIMENSIONS.append(PLAYER_ICON_WIDTH)
ICON_DIMENSIONS.append(PUNCH_ICON_WIDTH)
ICON_DIMENSIONS.append(KICK_ICON_WIDTH)
ICON_DIMENSIONS.append(KICK_ICON_HEIGTH)


# creating game window & setting display fonts
gameWindow = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGTH))
STAT_FONT = pygame.font.SysFont("comicsans", 16)
pygame.display.set_caption("DoucheBags SAGA")

# FIX PARAMETERS FOR GAME
SCREEN_UPDATE_CLOCK_TICK = 60
ZERO_DIVIDE_THRESHOLD = 0.000001 # sensitivity against divide by zero error
MOVE_TIME_WAIT=0.2        # seconds to wait before getting continuously pressed move button
HIT_ICON_SHOW_DURATION=0.5 # show hit icon x-seconds
POINTER_COLOR = (255,0,0)
POINTER_WIDTH = 2
POINTER_LENGTH = PLAYER_ICON_WIDTH/2+8
POINTER_FEATURES=[]
POINTER_FEATURES.append(POINTER_LENGTH)
POINTER_FEATURES.append(POINTER_WIDTH)
POINTER_FEATURES.append(POINTER_COLOR)
SOUND_BUTTON_X = 10
SOUND_BUTTON_Y = 10

# IMAGES FOR GAME
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "bg_img_white.png")).convert_alpha(), (WIN_WIDTH-2*FRAME_WIDTH, WIN_HEIGTH-2*FRAME_WIDTH))
frame_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "frame.jpg")).convert_alpha(), (WIN_WIDTH, WIN_HEIGTH))
player_img1 = pygame.transform.scale(pygame.image.load(os.path.join("Images", "trump.jpg")).convert_alpha(), (PLAYER_ICON_WIDTH, PLAYER_ICON_WIDTH))
player_img2 = pygame.transform.scale(pygame.image.load(os.path.join("Images", "putin.jpg")).convert_alpha(), (PLAYER_ICON_WIDTH, PLAYER_ICON_WIDTH))
punch_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "punch.png")).convert_alpha(), (PUNCH_ICON_WIDTH, PUNCH_ICON_HEIGTH))
kick_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "kick.png")).convert_alpha(), (KICK_ICON_WIDTH, KICK_ICON_HEIGTH))
hit_volume_on_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "hit_volume_on.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
hit_volume_off_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "hit_volume_off.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
bg_volume_on_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "background_volume_on.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
bg_volume_off_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "background_volume_off.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))


# Sound settings
bg_music='Sounds\EOTW.wav'
hit_try_music = 'Sounds\whooshW.wav'
hit_success_music = 'Sounds\punchW.wav'

game_sound_mixer = pygame.mixer
game_sound_mixer.init()
game_sound_mixer.Channel(0).set_volume(0.05)
game_sound_mixer.Channel(1).set_volume(0.8)
game_sound_mixer.Channel(2).set_volume(0.8)
game_sound_mixer.Channel(0).play(game_sound_mixer.Sound(bg_music),-1)

def changeState(state):
    if state == "ON":
        new_state = "OFF"
    elif state == "OFF":
        new_state = "ON"
    return new_state

def draw_frame(win, color, framed_win_dimensions):
    pygame.draw.rect(win, color, (0,0,framed_win_dimensions[2],framed_win_dimensions[1]))
    pygame.draw.rect(win, color, (0, 0, framed_win_dimensions[0], framed_win_dimensions[2]))
    pygame.draw.rect(win, color, (0, framed_win_dimensions[1]-framed_win_dimensions[2], framed_win_dimensions[0], framed_win_dimensions[2]))
    pygame.draw.rect(win, color, (framed_win_dimensions[0]-framed_win_dimensions[2], 0, framed_win_dimensions[2], framed_win_dimensions[1]))

def draw_window(win, players, sound_buttons, pointer_features, icon_dimensions, framed_win_dimensions, frame_color, stat_font, zero_divide_threshold, hit_icon_show_duration):
    win.fill((255,255,255))
    draw_frame(win,frame_color,framed_win_dimensions)
    #win.blit(frame_img, (0, 0))

    sound_buttons.drawSoundButton(win,bg_volume_on_img, bg_volume_off_img, hit_volume_on_img, hit_volume_off_img)
    for player in players:
        player.drawPlayer(win, icon_dimensions[0], stat_font)
        player.drawPointer(win, icon_dimensions[0], pointer_features, zero_divide_threshold)

    for player in players:
        player.drawHit(win, punch_img, kick_img, icon_dimensions[0], icon_dimensions[1], icon_dimensions[2], zero_divide_threshold, hit_icon_show_duration)
    pygame.display.update()

if __name__ == '__main__':
    Player1 = Player(1, 100, 100, "left", player_img1)
    Player2 = Player(2, 450, 300, "right", player_img2)
    SoundButtons = SoundButton(SOUND_BUTTON_X,SOUND_BUTTON_Y,VOLUME_BUTTON_WIDTH)
    Players=[]
    Players.append(Player1)
    Players.append(Player2)
    clock = pygame.time.Clock()
    direction = "unalter"
    hitType = "NONE"
    hitBool = 1
    run = True
    while run:
        clock.tick(SCREEN_UPDATE_CLOCK_TICK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

            # mouse clicks for sound buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx >= SOUND_BUTTON_X+2 and mx <= SOUND_BUTTON_X + VOLUME_BUTTON_WIDTH-2 and my >= SOUND_BUTTON_Y+2 and my <= SOUND_BUTTON_Y + VOLUME_BUTTON_WIDTH-2:
                    SoundButtons.setSoundState("BG", changeState(SoundButtons.getSoundState("BG")))

                if mx >= SOUND_BUTTON_X+VOLUME_BUTTON_WIDTH+2 and mx <= SOUND_BUTTON_X + 2*VOLUME_BUTTON_WIDTH-2 and my >= SOUND_BUTTON_Y+2 and my <= SOUND_BUTTON_Y + VOLUME_BUTTON_WIDTH-2:
                    SoundButtons.setSoundState("KICK", changeState(SoundButtons.getSoundState("KICK")))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hitType = "PUNCH"
                if event.key == pygame.K_s:
                    hitType = "KICK"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hitBool = 1
                if event.key == pygame.K_s:
                    hitBool = 1

        if hitBool == 0:
            hitType = "NONE"

        hit_info = Player1.hit(hitType, game_sound_mixer, hit_try_music, punch_img, kick_img, PUNCH_ICON_WIDTH, KICK_ICON_WIDTH, PLAYER_ICON_WIDTH, ZERO_DIVIDE_THRESHOLD)
        if hit_info[0] == "YES":
            hit_rect = hit_info[1]
            player_id = Player1.getID()
            for player in Players:
                check_id = player.getID()
                if player_id != check_id:
                    check_rect = player.getPlayerRect()
                    hit_success = hit_rect.colliderect(check_rect)
                    if hit_success == 1:
                        game_sound_mixer.Channel(2).play(game_sound_mixer.Sound(hit_success_music))
                        player.updateHealth(-Player1.getDamage(hitType))
                        Player1.updateScore(1)
        hitType = "NONE"


        Player1.move(MOVE_TIME_WAIT, WIN_WIDTH , WIN_HEIGTH, FRAME_WIDTH, PLAYER_ICON_WIDTH)
        draw_window(gameWindow, Players, SoundButtons, POINTER_FEATURES, ICON_DIMENSIONS, FRAMED_WIN_DIMENSIONS, FRAME_COLOR, STAT_FONT, ZERO_DIVIDE_THRESHOLD, HIT_ICON_SHOW_DURATION)
        if SoundButtons.getSoundState("BG") == "OFF":
            game_sound_mixer.Channel(0).set_volume(0)
        elif SoundButtons.getSoundState("BG") == "ON":
            game_sound_mixer.Channel(0).set_volume(0.05)

        if SoundButtons.getSoundState("KICK") == "OFF":
            game_sound_mixer.Channel(1).set_volume(0)
            game_sound_mixer.Channel(2).set_volume(0)
        elif SoundButtons.getSoundState("BG") == "ON":
            game_sound_mixer.Channel(1).set_volume(0.8)
            game_sound_mixer.Channel(2).set_volume(0.8)





