from player import Player, PlayerInfo
import time
import pygame
import os
from buttons import SoundButton, ConnectButton, NameButton, CloseGameButton, HitLoadButton
from network import Network
from logprocess import LogInfo



pygame.font.init()  # init font
pygame.init()


# WINDOW & IMAGE DIMENSIONS
WIN_WIDTH = 900
WIN_HEIGTH = 600
FRAME_WIDTH=50
FRAMED_WIN_DIMENSIONS = [WIN_WIDTH, WIN_HEIGTH, FRAME_WIDTH]
FRAME_COLOR=(0,100,150)
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
CONNECT_BUTTON_WIDTH= 200
CONNECT_BUTTON_HEIGTH = 70
POTION_ICON_WIDTH = 25
POTION_ICON_HEIGTH = 25


# creating game window & setting display fonts
gameWindow = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGTH), pygame.RESIZABLE)
STAT_FONT = pygame.font.SysFont("comicsans", 16)
GAMEOVER_FONT = pygame.font.SysFont("comicsans", 40)
pygame.display.set_caption("Welcome to DoucheBags Land")

# FIX PARAMETERS FOR GAME
SCREEN_UPDATE_CLOCK_TICK_INIT = 60
SCREEN_UPDATE_CLOCK_TICK_GAME = 30
GAME_OVER_SCREEN_TIME = 3
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
CONNECT_BUTTON_X = WIN_WIDTH/2
CONNECT_BUTTON_Y = WIN_HEIGTH/2
EXIT_BUTTON_X = SOUND_BUTTON_X + 2*VOLUME_BUTTON_WIDTH + 5
EXIT_BUTTON_Y = SOUND_BUTTON_Y
EXIT_BUTTON_WIDTH = 100
EXIT_BUTTON_HEIGTH = VOLUME_BUTTON_WIDTH
LEAVE_BUTTON_X = SOUND_BUTTON_X + 2*VOLUME_BUTTON_WIDTH + EXIT_BUTTON_WIDTH + 10
LEAVE_BUTTON_Y = SOUND_BUTTON_Y
LEAVE_BUTTON_WIDTH = 120
LEAVE_BUTTON_HEIGTH = VOLUME_BUTTON_WIDTH
PUNCH_WAIT = 4
KICK_WAIT = 7
WELCOME_TEXT=["YOU ARE NOW ENTERING","DOUCHEBAGS' LAND","BE CAREFUL..."]


# IMAGES FOR GAME
punch_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "punch.png")).convert_alpha(), (PUNCH_ICON_WIDTH, PUNCH_ICON_HEIGTH))
kick_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "kick.png")).convert_alpha(), (KICK_ICON_WIDTH, KICK_ICON_HEIGTH))
hit_volume_on_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "hit_volume_on.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
hit_volume_off_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "hit_volume_off.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
bg_volume_on_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "background_volume_on.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
bg_volume_off_img =pygame.transform.scale(pygame.image.load(os.path.join("Images", "background_volume_off.png")).convert_alpha(), (VOLUME_BUTTON_WIDTH, VOLUME_BUTTON_WIDTH))
health_potion_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "health.png")).convert_alpha(), (POTION_ICON_WIDTH, POTION_ICON_HEIGTH))
rapid_hit_potion_img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "rapid_hit.jpg")).convert_alpha(), (POTION_ICON_WIDTH, POTION_ICON_HEIGTH))


# Sound settings
BG_SOUND_LEVEL=0.0
HIT_SOUND_LEVEL=0.0
bg_music='Sounds\EOTW.wav'
hit_try_music = 'Sounds\whooshW.wav'
hit_success_music = 'Sounds\punchW.wav'

game_sound_mixer = pygame.mixer
game_sound_mixer.init()
game_sound_mixer.Channel(0).set_volume(HIT_SOUND_LEVEL)
game_sound_mixer.Channel(1).set_volume(HIT_SOUND_LEVEL)
game_sound_mixer.Channel(2).set_volume(HIT_SOUND_LEVEL)
game_sound_mixer.Channel(0).play(game_sound_mixer.Sound(bg_music),-1)

# read from logInfo
newLog = LogInfo("Logs/Profile.txt")
if not newLog.corruptFile:
    playerLog = newLog.getLog()
else:
    playerLog =["", 0, 0, 0, 20, 4, 7]

# initializations
playerReady = False


def split_init_info(init_message):
    splitted = init_message.split(",")
    return splitted

def update_display_dimensions(display):
    winfo = display.get_window_size()
    WIN_WIDTH = winfo[0]
    WIN_HEIGTH = winfo[1]
    FRAMED_WIN_DIMENSIONS[0] = WIN_WIDTH
    FRAMED_WIN_DIMENSIONS[1] = WIN_HEIGTH
    connectButton.x = int(FRAMED_WIN_DIMENSIONS[0]/2)-100
    connectButton.y = int(FRAMED_WIN_DIMENSIONS[1]/2)-100


def calculateGold(playerLog, newScore):
    score_diff = max(0,newScore - playerLog[2])
    gainedCoin = (playerLog[1]+1)*(score_diff*5)
    return gainedCoin

def getIcon(icon_num):
    if icon_num == 1:
        img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "trump.jpg")).convert_alpha(),
                                             (PLAYER_ICON_WIDTH, PLAYER_ICON_WIDTH))
    elif icon_num == 2:
        img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "putin.jpg")).convert_alpha(),
                                             (PLAYER_ICON_WIDTH, PLAYER_ICON_WIDTH))
    elif icon_num == 3:
        img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "recep.jpg")).convert_alpha(),
                                     (PLAYER_ICON_WIDTH, PLAYER_ICON_WIDTH))
    elif icon_num == 4:
        img = pygame.transform.scale(pygame.image.load(os.path.join("Images", "devlet.jpg")).convert_alpha(),
                                     (PLAYER_ICON_WIDTH, PLAYER_ICON_WIDTH))

    ort = "left"

    icon_info=[img, ort]
    return icon_info

def draw_top_scorers(listOfPlayerInfo):

    sorted_list = sorted(listOfPlayerInfo, key=lambda info: info.score, reverse=True)
    score_board_loc = (FRAMED_WIN_DIMENSIONS[0]-240, 80)
    size = (230, 20*len(sorted_list)+40)
    score_board_color=(0,30,100)
    score_board = pygame.Surface(size)
    score_board.set_alpha(50)
    score_board.fill(score_board_color)
    gameWindow.blit(score_board,score_board_loc)
    font = pygame.font.SysFont("comicsans", 30)
    display_text = font.render("Top Scorers", 1, (255, 0, 0))
    display_text.set_alpha(50)
    gameWindow.blit(display_text, (score_board_loc[0] +10, score_board_loc[1]+2))
    count=1
    font = pygame.font.SysFont("comicsans", 26)
    for info in sorted_list:
        display_text = font.render(info.name + ": " + str(info.score), 1, (0, 0, 0))
        display_text.set_alpha(50)
        gameWindow.blit(display_text, (score_board_loc[0]+3, score_board_loc[1]+count*25))
        count += 1


def draw_frame():
    #pygame.draw.rect(gameWindow, FRAME_COLOR, (0,0,FRAMED_WIN_DIMENSIONS[2],FRAMED_WIN_DIMENSIONS[1]))
    pygame.draw.rect(gameWindow, FRAME_COLOR, (0, 0, FRAMED_WIN_DIMENSIONS[0], FRAMED_WIN_DIMENSIONS[2]))
    #pygame.draw.rect(gameWindow, FRAME_COLOR, (0, FRAMED_WIN_DIMENSIONS[1]-FRAMED_WIN_DIMENSIONS[2], FRAMED_WIN_DIMENSIONS[0], FRAMED_WIN_DIMENSIONS[2]))
    #pygame.draw.rect(gameWindow, FRAME_COLOR, (FRAMED_WIN_DIMENSIONS[0]-FRAMED_WIN_DIMENSIONS[2], 0, FRAMED_WIN_DIMENSIONS[2], FRAMED_WIN_DIMENSIONS[1]))

def draw_all():
    gameWindow.fill((255, 255, 255))
    draw_frame()
    SoundButtons.drawSoundButton(gameWindow, bg_volume_on_img, bg_volume_off_img, hit_volume_on_img, hit_volume_off_img)
    exitGameButton.drawCloseButton(gameWindow)

def draw_potions(potionList):

    for potion in potionList:
        if potion[0] == "health":
            gameWindow.blit(health_potion_img, potion[1])
        if potion[0] == "rapid":
            gameWindow.blit(rapid_hit_potion_img, potion[1])

def draw_stage_name():
    draw_all()
    nameButton.drawNameButton(gameWindow, int(FRAMED_WIN_DIMENSIONS[0]/2)-100, int(FRAMED_WIN_DIMENSIONS[1]/2)-100)
    pygame.display.update()


def draw_stage_connect():
    draw_all()
    connectButton.drawConnectButton(gameWindow, int(FRAMED_WIN_DIMENSIONS[0]/2)-100, int(FRAMED_WIN_DIMENSIONS[1]/2)-100)
    pygame.display.update()

def draw_no_connection():
    draw_all()
    fonts = pygame.font.SysFont("comicsans", connectButton.font)
    display_text = fonts.render(str("No Connection to Server..."), 1, (0, 0, 0))
    run = True
    start_time = time.perf_counter()
    while run:
        current_time = time.perf_counter()
        if current_time - start_time > 1.5:
            run = False
        else:
            gameWindow.blit(display_text, (connectButton.x + 10, connectButton.y + 15))
            pygame.display.update()

def draw_stage_play(players, client_player_ID, topScorer, hit_load_button, potionList):
    draw_all()
    leaveRoomButton.drawCloseButton(gameWindow)

    draw_potions(potionList)
    for player in players:
        player.drawPlayer(gameWindow, ICON_DIMENSIONS[0], STAT_FONT)
        if player.getID() == client_player_ID:
            player.drawPointer(gameWindow, ICON_DIMENSIONS[0], POINTER_FEATURES, ZERO_DIVIDE_THRESHOLD)

    for player in players:
        player.drawHit(gameWindow, punch_img, kick_img, ICON_DIMENSIONS[0], ICON_DIMENSIONS[1], ICON_DIMENSIONS[2], ZERO_DIVIDE_THRESHOLD, HIT_ICON_SHOW_DURATION)

    if topScorer:
        draw_top_scorers(players)
    hit_load_button.drawHitLoad(gameWindow, FRAMED_WIN_DIMENSIONS[0]-100, FRAMED_WIN_DIMENSIONS[1]-100)
    pygame.display.update()

def run_game_welcome():
    # initialize title
    pygame.display.set_caption("Welcome to DoucheBags Land")
    game_stage = "name"

    """curr_time = time.perf_counter()

    for ii in range(len(WELCOME_TEXT)):

        text = WELCOME_TEXT[ii]
        for ll in range(len(text)):
                wait = True
                while wait:
                    if time.perf_counter() - curr_time > 0.15:
                        curr_time = time.perf_counter()
                        wait = False
                font = pygame.font.SysFont("comicsans", 30)
                display_text = font.render(text[0:ll+1], 1, (0, 100, 150))
                gameWindow.blit(display_text, (int(FRAMED_WIN_DIMENSIONS[0]/2)-100, int(FRAMED_WIN_DIMENSIONS[1]/2)-100+ii*30))
                pygame.display.update()
    game_stage = "name"
    wait = True
    while wait:
        if time.perf_counter() - curr_time > 1:
            curr_time = time.perf_counter()
            wait = False"""
    return game_stage


def run_game_stage_name():
    global playerLog


    name = nameButton.name
    gotName = False
    while gotName == False:

        clock.tick(SCREEN_UPDATE_CLOCK_TICK_INIT)

        # getting the new screen dimensions
        update_display_dimensions(pygame.display)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if len(name) < 10:
                    name += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    gotName = True
                    game_stage = "connect"
                    break
            elif event.type == pygame.QUIT:
                gotName = True
                game_stage = "closing"
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                SoundButtons.mouseAction(mx, my)
                connectButton.mouseAction(mx, my)
                exitGameButton.mouseAction(mx, my)
                if exitGameButton.clicked:
                    game_stage = "closing"
                    gotName = True

        # adjust the background and hit sounds
        if SoundButtons.bg_sound == False:
            game_sound_mixer.Channel(0).set_volume(0)
        elif SoundButtons.bg_sound == True:
            game_sound_mixer.Channel(0).set_volume(BG_SOUND_LEVEL)

        if SoundButtons.kick_sound == False:
            game_sound_mixer.Channel(1).set_volume(0)
            game_sound_mixer.Channel(2).set_volume(0)
        elif SoundButtons.kick_sound == True:
            game_sound_mixer.Channel(1).set_volume(HIT_SOUND_LEVEL)
            game_sound_mixer.Channel(2).set_volume(HIT_SOUND_LEVEL)

        nameButton.name = name
        playerLog[0] = name
        draw_stage_name()
    return game_stage


def run_game_stage_connect():
    global playerReady

    connectButton.reset()
    # Initial Phase before connecting to server
    while playerReady == False:

        # getting the new screen dimensions
        update_display_dimensions(pygame.display)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                playerReady = True
                game_stage = "closing"
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                SoundButtons.mouseAction(mx, my)
                connectButton.mouseAction(mx, my)
                exitGameButton.mouseAction(mx, my)
                if exitGameButton.clicked:
                    game_stage = "closing"
                    playerReady = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    connectButton.clicked = True
                    connectButton.text = "Connecting to Server..."
                    connectButton.font = 30

        if connectButton.clicked == True:
            playerReady = True
            game_stage = "play"

        # adjust the background and hit sounds
        if SoundButtons.bg_sound == False:
            game_sound_mixer.Channel(0).set_volume(0)
        elif SoundButtons.bg_sound == True:
            game_sound_mixer.Channel(0).set_volume(BG_SOUND_LEVEL)

        if SoundButtons.kick_sound == False:
            game_sound_mixer.Channel(1).set_volume(0)
            game_sound_mixer.Channel(2).set_volume(0)
        elif SoundButtons.kick_sound == True:
            game_sound_mixer.Channel(1).set_volume(HIT_SOUND_LEVEL)
            game_sound_mixer.Channel(2).set_volume(HIT_SOUND_LEVEL)

        # update the display window
        draw_stage_connect()

        # wait time
        clock.tick(SCREEN_UPDATE_CLOCK_TICK_INIT)


    connectButton.clicked = False
    return game_stage


def run_game_stage_play():
        topScorer = True
        server_communicate = True
        client_player_info =[]
        hitLoadButton = HitLoadButton(playerLog[5], playerLog[6])

        # Ready to connect to server
        net = Network()
        print("receiving: ", net.init_info)

        # if no connection to server
        if not net.init_info:
            draw_no_connection()
            server_communicate = False
            game_stage = "name"

        if server_communicate == True:

            # initial info from server: game ID, player_ID, pos_x, pos_y, icon_num
            init_player_info = split_init_info(net.init_info)
            game_ID = int(init_player_info[0])
            pygame.display.set_caption("Connected to Room "+ str(game_ID))
            client_player_ID = int(init_player_info[1])
            pos_x = int(init_player_info[2])
            pos_y = int(init_player_info[3])
            icon_num = int(init_player_info[4])
            icon_info = getIcon(icon_num)

            # create client Player object
            client_player = Player(client_player_ID, nameButton.name, pos_x, pos_y, icon_info[0], icon_info[1], icon_num,[], 0, int(playerLog[4]), playerLog[5], playerLog[6])

            # create client PlayerInfo object
            client_player_info = PlayerInfo(client_player,[])
            run = True


            # check keyboard & mouse actions
            hitType = "NONE"
            hitBool = 1
            rapid_hit = False
            while run:
                obtained_potion_IDs=[]
                clock.tick(SCREEN_UPDATE_CLOCK_TICK_GAME)

                # getting the new screen dimensions
                update_display_dimensions(pygame.display)


                # sending the new player list from server while sending the updated player
                if client_player_info.health <= 0:
                    game_stage = "game_over"
                    run = False
                else:
                    try:
                        net.send(client_player_info)
                    except:
                        draw_no_connection()
                        game_stage = "stat_info"
                        run = False
                        net.close()
                        break

                    # receiving the new player list info from server
                    try:
                        game = net.receive()
                    except:
                        draw_no_connection()
                        game_stage = "game_over"
                        net.close()
                        run = False
                        break

                    playerInfoList = game.playerInfoList
                    if not playerInfoList:
                        draw_no_connection()
                        game_stage = "game_over"
                        run = False
                        break

                    # updating the current player
                    for info in playerInfoList:

                        if info.id == client_player_ID:
                            client_player.copy(info)

                    players = []
                    players.append(client_player)

                    for info in playerInfoList:

                        if info.id != client_player_ID:
                           icon_info = getIcon(info.icon_num)
                           other_player = Player(info.id, info.name, info.x, info.y, icon_info[0], icon_info[1], icon_num, info.hitList, info.score, info.health, PUNCH_WAIT, KICK_WAIT)
                           players.append(other_player)


                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            run = False
                            game_stage = "closing"
                            net.close()
                            break

                        # checking mouse clicks for updating sound buttons & sounds
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = pygame.mouse.get_pos()
                            SoundButtons.mouseAction(mx, my)
                            exitGameButton.mouseAction(mx, my)
                            leaveRoomButton.mouseAction(mx,my)
                            if exitGameButton.clicked:
                                net.close()
                                game_stage = "closing"
                                run = False
                            if leaveRoomButton.clicked:
                                net.close()
                                game_stage = "game_over"
                                leaveRoomButton.clicked = False
                                run = False

                        # checking keyboard inputs for hitting
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
                            if event.key == pygame.K_w:
                                topScorer = not topScorer


                    if hitBool == 0:
                        hitType = "NONE"


                    # updating player location : keyboard input checks are done inside the function
                    client_player.move(MOVE_TIME_WAIT, FRAMED_WIN_DIMENSIONS[0], FRAMED_WIN_DIMENSIONS[1], FRAME_WIDTH, PLAYER_ICON_WIDTH, ZERO_DIVIDE_THRESHOLD)

                    # check if player gets any potion
                    client_rect = client_player.getPlayerRect()
                    for potion in game.potionList:
                        potion_rect = health_potion_img.get_rect(topleft=potion[1])
                        getPotion = client_rect.colliderect(potion_rect)
                        if getPotion:
                            obtained_potion_IDs.append(potion[2])
                            if potion[0] == "health":
                                client_player.health += 3
                            if potion[0] == "rapid":
                                start_counter = time.perf_counter()
                                rapid_hit = True

                    if rapid_hit == True:
                        if time.perf_counter()-start_counter > 10:
                            rapid_hit = False
                            client_player.minPunchWait = PUNCH_WAIT
                            client_player.minKickWait = KICK_WAIT
                            hitLoadButton.punchWait = PUNCH_WAIT
                            hitLoadButton.kickWait = KICK_WAIT
                        else:
                            client_player.minPunchWait = PUNCH_WAIT/2
                            client_player.minKickWait = KICK_WAIT/2
                            hitLoadButton.punchWait = PUNCH_WAIT/2
                            hitLoadButton.kickWait = KICK_WAIT/2


                    # reset the hit list of client player & get the hit_info: (did_player_hit, the Rect object of hitting)
                    client_player.resetHitList()
                    hit_info = client_player.hit(hitType, game_sound_mixer, hit_try_music, punch_img, kick_img, PUNCH_ICON_WIDTH,
                                                 KICK_ICON_WIDTH, PLAYER_ICON_WIDTH, ZERO_DIVIDE_THRESHOLD)
                    if hit_info[0] == "YES":
                        hit_rect = hit_info[1]

                    #update hit load buttons
                    hitLoadButton.lastHitTime = client_player.lastHitTime
                    hitLoadButton.updateHitLoad(time.perf_counter())


                    # update player health if other players hit matches the client ID
                    # update the hit list of the client (other player IDs & damage performed )
                    # based on collision check of client hit Rect & other player icon Rect object
                    for player in players:
                        check_id = player.getID()
                        if check_id != client_player_ID:
                            # check if the client player is hit by other players & update the health points
                            for hits in player.getHitList():
                                if hits[0] == client_player_ID:
                                    game_sound_mixer.Channel(2).play(game_sound_mixer.Sound(hit_success_music))
                                    client_player.health -= hits[1]


                            # check if the client player manage to hit other players & update the client players hit list & sounds
                            if hit_info[0] == "YES":
                                check_rect = player.getPlayerRect()
                                hit_success = hit_rect.colliderect(check_rect)
                                if hit_success == 1:
                                    game_sound_mixer.Channel(2).play(game_sound_mixer.Sound(hit_success_music))
                                    client_player.updateHitList(check_id, client_player.getDamage(hitType))
                                    client_player.score += 1

                    draw_stage_play(players, client_player_ID, topScorer, hitLoadButton, game.potionList)
                    hitType = "NONE"
                    client_player_info = PlayerInfo(client_player, obtained_potion_IDs)

                    # adjust the background and hit sounds
                    if SoundButtons.bg_sound == False:
                        game_sound_mixer.Channel(0).set_volume(0)
                    elif SoundButtons.bg_sound == True:
                        game_sound_mixer.Channel(0).set_volume(BG_SOUND_LEVEL)

                    if SoundButtons.kick_sound == False:
                        game_sound_mixer.Channel(1).set_volume(0)
                        game_sound_mixer.Channel(2).set_volume(0)
                    elif SoundButtons.kick_sound == True:
                        game_sound_mixer.Channel(1).set_volume(HIT_SOUND_LEVEL)
                        game_sound_mixer.Channel(2).set_volume(HIT_SOUND_LEVEL)

        return (game_stage, client_player_info)

def run_game_stage_game_over(client_player_info):
    global playerLog
    newGold = calculateGold(playerLog, client_player_info.score)
    run = True
    start_time = time.perf_counter()
    game_stage = "name"
    for ii in range(2):
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    ii = 1
                    game_stage = "closing"
                    break

            disp_loc=(int(FRAMED_WIN_DIMENSIONS[0]/2)-100, int(FRAMED_WIN_DIMENSIONS[1]/2))
            current_time = time.perf_counter()
            if current_time-start_time > GAME_OVER_SCREEN_TIME:
                start_time = current_time
                run = False
            else:
                draw_all()
                if ii == 0:
                    text = "GAME OVER"
                elif ii == 1:
                    text = "Your Score: " + str(client_player_info.score)
                game_over_text = GAMEOVER_FONT.render(text, 1, (255, 1, 1))
                gameWindow.blit(game_over_text, disp_loc)
                pygame.display.update()

    start_time = time.perf_counter()
    if client_player_info.score > playerLog[2] and game_stage != "closing":

        for ii in range(2):
            run = True
            while run:
                for event in events:
                    if event.type == pygame.QUIT:
                        run = False
                        ii = 1
                        game_stage = "closing"
                        break

                disp_loc = (int(FRAMED_WIN_DIMENSIONS[0] / 2) - 100, int(FRAMED_WIN_DIMENSIONS[1] / 2))
                current_time = time.perf_counter()
                if current_time - start_time > GAME_OVER_SCREEN_TIME:
                    start_time = current_time
                    run = False
                else:
                    draw_all()
                    if ii == 0:
                        text = "New Best Score: " + str(client_player_info.score)
                        game_over_text = GAMEOVER_FONT.render(text, 1, (255, 1, 1))
                        gameWindow.blit(game_over_text, disp_loc)
                    elif ii == 1:
                        text1 = "Gained Coins: " + str(int(newGold))
                        text2 = "You Reached: " + str(int(newGold + playerLog[3])) + " Coins"
                        game_over_text = GAMEOVER_FONT.render(text1, 1, (255, 1, 1))
                        gameWindow.blit(game_over_text, disp_loc)
                        game_over_text = GAMEOVER_FONT.render(text2, 1, (255, 1, 1))
                        gameWindow.blit(game_over_text, (disp_loc[0],disp_loc[1]+40))

                    pygame.display.update()

    return game_stage

if __name__ == '__main__':

    # initialize the buttons
    SoundButtons = SoundButton(SOUND_BUTTON_X, SOUND_BUTTON_Y, VOLUME_BUTTON_WIDTH)
    connectButton = ConnectButton(CONNECT_BUTTON_WIDTH, CONNECT_BUTTON_HEIGTH)
    nameButton = NameButton(CONNECT_BUTTON_WIDTH, CONNECT_BUTTON_HEIGTH, playerLog[0])
    exitGameButton = CloseGameButton(EXIT_BUTTON_X, EXIT_BUTTON_Y, EXIT_BUTTON_WIDTH, EXIT_BUTTON_HEIGTH, "Exit Game")
    leaveRoomButton = CloseGameButton(LEAVE_BUTTON_X, LEAVE_BUTTON_Y, LEAVE_BUTTON_WIDTH, LEAVE_BUTTON_HEIGTH, "Leave Room")

    # initialize the game stage: g1: type-select -> g2: name-select -> g3: connect & play -> g1
    game_stage = "welcome"

    # intialize clock
    clock = pygame.time.Clock()

    # initialize game application
    run_game_app = True

    while run_game_app:

        if game_stage == "welcome":
            game_stage = run_game_welcome()
        elif game_stage == "name":
            game_stage = run_game_stage_name()
            playerReady = False
        elif game_stage == "connect":
            game_stage = run_game_stage_connect()
        elif game_stage == "play":
            game_info = run_game_stage_play()
            game_stage = game_info[0]
            client_info = game_info[1]
        elif game_stage == "game_over":
            game_stage = run_game_stage_game_over(client_info)
        elif game_stage == "closing":
            newGold = calculateGold(playerLog, client_info.score)
            playerLog[2] = client_info.score
            playerLog[3] = newGold+playerLog[3]
            newLog.modify(playerLog)
            newLog.writeFile()
            run_game_app = False

