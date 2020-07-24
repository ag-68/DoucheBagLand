import pygame


pygame.font.init()  # init font
pygame.init()

# WINDOW & ICON & DOCK BUTTON DIMENSIONS and Locations
WIN_DIM = [900, 600, 50] # width heigth frame-heigth
ICON_DIM = [50, 50, 30, 30, 70, 40, 25, 25, 80, 40] # width/heigth for player(0-1), punch(2-3), kick(4-5), potion(6-7)
DOCK_BUT_DIM = [30, 30, 100, 30, 120, 30, 75, 30, 120, 30] #width/heigth for dock buttons: volume(0-1)/exit(2-3)/leave(4-5)/back(6-7)/go to shop (8-9)
DOCK_BUT_LOC = [10, 10, 75, 10, 180, 10, 180, 10, 180, 10] # x-y location of buttons: " "
RECT_DIM = [200, 70, 80, 40, 150, 150, 110, 110] # rectangle width/heights for player name(0-1) / hit-health cond (2-3) / shop item (4-5) / shop item img (6-7)
RECT_LOC =[(WIN_DIM[0]+RECT_DIM[0])/2, (WIN_DIM[1]+RECT_DIM[1])/2, WIN_DIM[0]-3*RECT_DIM[2]-12, WIN_DIM[1]-RECT_DIM[3]-10, (WIN_DIM[0]-3*RECT_DIM[4])/2, (WIN_DIM[1]-RECT_DIM[5])/2]
# topleft corners of rect. of player name / hit health cond / first shop item

# FONTS
DISP_FONT="Arial"
FONT_SIZE = [30, 20, 24, 20, 26, 22, 20, 26, 26, 18, 16, 22]   # font sizes for welcome text (0) / dock buttons(1) /
# name rectange (2-3) / top scorers (4-5) / player condition (6) / game over texts(7) / shop (8-9) / player name on icon (10) / best score (11)

# COLORS
WELCOME_BG_COLOR = (0, 0, 0)
WELCOME_TEXT_COLOR = (0, 100, 150)
GAME_BG_COLOR = (255, 255, 255)
FRAME_COLOR = (0, 100, 150)
DOCK_BUT_COLOR = [(240, 240, 240), (0, 0, 0)] # rectangle / text
NAME_BUT_COLOR = [(0, 100, 150), (255, 255, 255), (255, 255, 255), (255, 0, 0)]  # outer rect / inner field rect / info text / input text
PLAYER_NAME_COLOR = (0, 0, 0)
TOP_SCORER_COLOR = [(200, 200, 200), (255, 0, 0), (0, 0, 0), (200, 100, 0)] # window / title / other player entry / player entry
HEALTH_FILL_COLOR = [(0, 255, 0), (75, 180, 0), (150, 100, 0), (250, 0, 0)] # from green to red based on health condition
HIT_FILL_COLOR = (200, 0, 0)
HIT_RECT_COLOR = (180, 180, 180)
HIT_TEXT_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)
SHOP_COLOR = [(0, 0, 0), (250, 250, 250), (125, 125, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0)] # remaining coin / item window / item info text / item cost text / quest. win / quest. text
RECT_BORDER_COLOR = (0, 0, 0)

# ALPHA VALUES (TRANSPARENCY)
ALPHA_VAL = [50, 80, 30, 60, 75, 175, 250] # topscorer board & other player and player (0-1) / condition rect & text (2-3) / shop inactive - touch - click (4-5-6)

# WAITING TIMES
SCREEN_UPDATE_CLOCK_TICK_INIT = 60
SCREEN_UPDATE_CLOCK_TICK_GAME = 30
GAME_OVER_SCREEN_TIME = 3
MOVE_TIME_WAIT = 0.0  # seconds to wait before getting continuously pressed move button
HIT_ICON_DURATION = 0.65  # show hit icon x-seconds

# TEXTS
WELCOME_TEXT = ["YOU ARE NOW ENTERING", "DOUCHEBAGS' LAND", "BE CAREFUL..."]
CAPTION_TEXT = "Welcome to DoucheBags Land"

# SOUNDS
BG_SOUND_LEVEL = 0.016
HIT_SOUND_LEVEL = 0.04
bg_music = 'EOTW45.wav'
hit_try_music = 'whooshW.wav'
hit_success_music = 'punchW.wav'
ko_music = 'KO.wav'

# POINTER
POINTER_FEATURES = [(255, 0, 0), 2, ICON_DIM[0]/2+8] # pointer color, width, length

#LEVELS

LEVEL_PTS = [100, 250, 500, 1000,  5000, 10000]
LEVEL_NAME = ["LOSER", "CABRON", "BASTARD", "JACKAL", "SHARK", "DOUCHEBAG"]
LEVEL_TEXT = ["You suck...:Get lost and try harder !", "Don't celebrate yet Cabron!:Your ass is not safe...", "Proud to be Mr. Bastard?:You are a joke...", "Jackals don't live too long...:Keep fighting for a happy life", "You pay college to become Shark?:You need more education !", "Congrats now you are a total Douchebag:Even I didn't expect this and so did your parents..."]
# OTHER
ZERO_THR = 0.000001  # sensitivity against zero e.g. divide or compare


