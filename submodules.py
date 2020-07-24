import settings
import inits
import math


def split_init_info(init_message):
    splitted = init_message.split(",")
    return splitted

def update_display_dimensions(display):
    winfo = display.get_window_size()
    settings.WIN_DIM[0] = winfo[0]
    settings.WIN_DIM[1] = winfo[1]

    inits.health_shop_button.x = (settings.WIN_DIM[0]-3*settings.RECT_DIM[4])/2-10
    inits.health_shop_button.y = (settings.WIN_DIM[1]-settings.RECT_DIM[5])/2
    inits.hit_speed_shop_button.x = inits.health_shop_button.x + settings.RECT_DIM[4] + 10
    inits.hit_speed_shop_button.y = inits.health_shop_button.y
    inits.damage_shop_button.x = inits.hit_speed_shop_button.x + settings.RECT_DIM[4] + 10
    inits.damage_shop_button.y = inits.health_shop_button.y


def calculateGold(newScore):
    gainedCoin = (inits.playerLog["Level"]+1)*newScore*5
    return gainedCoin

def calcHealthUpg():
    cost = math.pow(1.25, inits.playerLog["HealthUp"])*130
    quot = cost / 25
    cost = 25 * math.ceil(quot)
    return cost

def calcHitSpeedUpg():
    cost = math.pow(1.15, inits.playerLog["HitSpeedUp"])*100
    quot = cost / 25
    cost = 25 * math.ceil(quot)
    return cost

def calcDamageUpg():
    cost = math.pow(1.2, inits.playerLog["HitDamageUp"])*120
    quot = cost / 25
    cost = 25 * math.ceil(quot)
    return cost

def getIcon(icon_num):
    if icon_num == 1:
        img = inits.trump_img
    elif icon_num == 2:
        img = inits.putin_img
    elif icon_num == 3:
        img = inits.recep_img
    elif icon_num == 4:
        img = inits.devlet_img

    ort = "left"

    icon_info=[img, ort]
    return icon_info