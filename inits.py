import settings
import pygame
import logprocess
import buttons
import os


# INITIALIZATIONS
pygame.init()
pygame.font.init()
gameDisp = pygame.display
gameDisp.init()

# creating game window & setting display fonts
gameWindow = gameDisp.set_mode((settings.WIN_DIM[0], settings.WIN_DIM[1]), pygame.RESIZABLE)
gameDisp.set_caption("Welcome to DoucheBags Land")


# IMAGES FOR GAME
trump_img = pygame.transform.scale(pygame.image.load("trump.png").convert_alpha(),
                                             (settings.ICON_DIM[0], settings.ICON_DIM[1]))

putin_img = pygame.transform.scale(pygame.image.load("putin.jpg").convert_alpha(),
                                             (settings.ICON_DIM[0], settings.ICON_DIM[1]))

recep_img = pygame.transform.scale(pygame.image.load("recep.png").convert_alpha(),
                                     (settings.ICON_DIM[0], settings.ICON_DIM[1]))

devlet_img = pygame.transform.scale(pygame.image.load("devlet.png").convert_alpha(),
                                     (settings.ICON_DIM[0], settings.ICON_DIM[1]))

punch_img = pygame.transform.scale(pygame.image.load("punch.png").convert_alpha(),
                                   (settings.ICON_DIM[2], settings.ICON_DIM[3]))
kick_img = pygame.transform.scale(pygame.image.load("kick.png").convert_alpha(),
                                  (settings.ICON_DIM[4], settings.ICON_DIM[5]))
ko_img = pygame.transform.scale(pygame.image.load("KO.jpg").convert_alpha(),
                                  (settings.ICON_DIM[0]-10, settings.ICON_DIM[1]-10))
hit_volume_on_img = pygame.transform.scale(
    pygame.image.load("hit_volume_on.png").convert_alpha(),
    (settings.DOCK_BUT_DIM[0], settings.DOCK_BUT_DIM[1]))
hit_volume_off_img = pygame.transform.scale(
    pygame.image.load("hit_volume_off.png").convert_alpha(),
    (settings.DOCK_BUT_DIM[0], settings.DOCK_BUT_DIM[1]))
bg_volume_on_img = pygame.transform.scale(
    pygame.image.load("background_volume_on.png").convert_alpha(),
    (settings.DOCK_BUT_DIM[0], settings.DOCK_BUT_DIM[1]))
bg_volume_off_img = pygame.transform.scale(
    pygame.image.load("background_volume_off.png").convert_alpha(),
    (settings.DOCK_BUT_DIM[0], settings.DOCK_BUT_DIM[1]))
health_potion_img = pygame.transform.scale(pygame.image.load("health.png").convert_alpha(),
                                           (settings.ICON_DIM[6], settings.ICON_DIM[7]))
rapid_hit_potion_img = pygame.transform.scale(
    pygame.image.load("rapid_hit.jpg").convert_alpha(), (settings.ICON_DIM[6], settings.ICON_DIM[7]))

health_shop_img = pygame.transform.scale(
    pygame.image.load("red_cross.jpg").convert_alpha(), (settings.RECT_DIM[6], settings.RECT_DIM[7]))
health_shop_img.set_alpha(10)

hit_speed_shop_img = pygame.transform.scale(
    pygame.image.load("rapid_hit.jpg").convert_alpha(), (settings.RECT_DIM[6], settings.RECT_DIM[7]))
hit_speed_shop_img.set_alpha(10)

hit_damage_shop_img = pygame.transform.scale(
    pygame.image.load("punch_strength.png").convert_alpha(), (settings.RECT_DIM[6], settings.RECT_DIM[7]))
hit_damage_shop_img.set_alpha(10)

# sound mixer
game_sound_mixer = pygame.mixer
game_sound_mixer.init()
game_sound_mixer.Channel(0).set_volume(settings.BG_SOUND_LEVEL)
game_sound_mixer.Channel(1).set_volume(settings.HIT_SOUND_LEVEL)
game_sound_mixer.Channel(2).set_volume(settings.HIT_SOUND_LEVEL)
game_sound_mixer.Channel(3).set_volume(settings.HIT_SOUND_LEVEL)
game_sound_mixer.Channel(0).play(game_sound_mixer.Sound(settings.bg_music), -1)

# read from logInfo (if file is corrupt then give default values)
newLog = logprocess.LogInfo("Profile.txt")
if not newLog.corruptFile:
    playerLog = newLog.profileLog
    print("plog: ", playerLog)
else:
    print("log is corrupt, setting default values...")
    attributeNameList = ["Name", "Level", "BestScore", "Coins", "HealthUp", "HitSpeedUp", "HitDamageUp", "Health",
                              "PunchWait", "KickWait", "PunchDamage", "KickDamage"]
    attributeVal = ["", 0, 0, 0, 0, 0, 0, 10, 4, 7, 3, 5]
    playerLog={}
    for idx, val in enumerate(attributeNameList):
        playerLog[attributeNameList[idx]] = attributeVal[idx]


# initialize buttons
SoundButtons = buttons.SoundButton(settings.DOCK_BUT_LOC[0], settings.DOCK_BUT_LOC[1], settings.DOCK_BUT_DIM[0])
nameButton = buttons.NameButton(settings.RECT_DIM[0], settings.RECT_DIM[1], playerLog["Name"])
exitGameButton = buttons.DockButton(settings.DOCK_BUT_LOC[2], settings.DOCK_BUT_LOC[3], settings.DOCK_BUT_DIM[2], settings.DOCK_BUT_DIM[3], "Exit Game")
leaveRoomButton = buttons.DockButton(settings.DOCK_BUT_LOC[4], settings.DOCK_BUT_LOC[5], settings.DOCK_BUT_DIM[4], settings.DOCK_BUT_DIM[5], "Leave Room")
backButton = buttons.DockButton(settings.DOCK_BUT_LOC[4], settings.DOCK_BUT_LOC[5], settings.DOCK_BUT_DIM[6], settings.DOCK_BUT_DIM[7], "Back")
goToShopButton = buttons.DockButton(settings.DOCK_BUT_LOC[4], settings.DOCK_BUT_LOC[5], settings.DOCK_BUT_DIM[4], settings.DOCK_BUT_DIM[5], "Go to Shop")

health_shop_button = buttons.ShopButton(settings.RECT_LOC[4], settings.RECT_LOC[5], settings.RECT_DIM[4], settings.RECT_DIM[5], "%5 Health Boost", 0, "health")
hit_speed_shop_button = buttons.ShopButton(settings.RECT_LOC[4]+settings.RECT_DIM[4]+10, settings.RECT_LOC[5], settings.RECT_DIM[4], settings.RECT_DIM[5], "%5 Hit Speed Boost", 0, "hit_speed")
damage_shop_button = buttons.ShopButton(settings.RECT_LOC[4]+2*settings.RECT_DIM[4]+10, settings.RECT_LOC[5], settings.RECT_DIM[4], settings.RECT_DIM[5], "%5 Damage Boost", 0, "damage")

# intialize clock
clock = pygame.time.Clock()