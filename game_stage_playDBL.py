import time
import settings
import inits
from buttons import HitLoadButton
import submodules
import routines
from player import Player, PlayerInfo
from network import Network
from game import Game
import drawings
import pickle


def run_game_stage_play():
    score = 0
    gainCoin = 0
    playerLogChange = False
    newBestScore = False
    newLevelGain = False
    game_stage = "game_over"
    topScorer = True
    player_condition = True
    server_communicate = True
    client_player_info = []

    hitLoadButton = HitLoadButton(inits.playerLog["PunchWait"], inits.playerLog["KickWait"], inits.playerLog["Health"])

    # Ready to connect to server
    net = Network()
    print("initial info: ", net.init_info)

    init_player_info=pickle.loads(net.init_info)
    print("Received Initial Player Info: ", init_player_info)

    # if no connection to server
    if not init_player_info:
        drawings.draw_no_connection()
        server_communicate = False
        game_stage = "name"

    if server_communicate == True:

        # initial info from server: game ID, player_ID, pos_x, pos_y, icon_num
        init_player_info = submodules.split_init_info(init_player_info )
        game_ID = int(init_player_info[0])
        inits.gameDisp.set_caption("Connected to Room " + str(game_ID))
        client_player_ID = int(init_player_info[1])
        pos_x = int(init_player_info[2])
        pos_y = int(init_player_info[3])
        icon_num = int(init_player_info[4])
        icon_info = submodules.getIcon(icon_num)

        # create client Player object
        posInfo = [pos_x, pos_y, 0, 0]
        hitInfo = [False, "right", (0, 0), [], 0, "NONE"]
        client_player = Player(client_player_ID, inits.nameButton.name, posInfo, icon_info[0], icon_info[1],
                               icon_num, hitInfo, 0, inits.playerLog["Health"], inits.playerLog["PunchWait"],
                               inits.playerLog["KickWait"], inits.playerLog["PunchDamage"],
                               inits.playerLog["KickDamage"])

        # create client PlayerInfo object
        client_player_info = PlayerInfo(client_player, [])
        run = True

        # check keyboard & mouse actions
        hitType = "NONE"
        hitBool = 1
        rapid_hit = False
        rx_time = time.perf_counter()
        while run:

            obtained_potion_IDs = []
            #inits.clock.tick(settings.SCREEN_UPDATE_CLOCK_TICK_GAME)

            # getting the new screen dimensions
            submodules.update_display_dimensions(inits.gameDisp)

            # sending the new player list from server while sending the updated player
            if client_player_info.health <= 0:
                game_stage = "game_over"
                run = False
                break
            else:
                tx_time = time.perf_counter()
                try:
                    net.send(client_player_info)
                except:
                    print("sending not successful")
                    drawings.draw_no_connection()
                    game_stage = "name"
                    run = False
                    net.close()
                    break
                #print("tx delay: ", tx_time - time.perf_counter())
                # receiving the new player list info from server
                #time.sleep(0.1)
                #print("process delay: ", rx_time - time.perf_counter())
                data = net.receive()
                game_data = pickle.loads(data)
                """try:
                    game_data = pickle.loads(data)
                except:
                    print("unknown error")"""
                #print("rx delay: ",  time.perf_counter()-rx_time)
                rx_time = time.perf_counter()
                game_IDX = game_data.game_ID
                playerInfoList = game_data.playerInfoList
                potionList = game_data.potionList

                if game_IDX < 0:
                    drawings.draw_no_connection()
                    game_stage = "name"
                    run = False
                    playerLogChange = False
                    net.close()
                    break
                else:
                    playerLogChange = True
                    # updating the current player
                    for info in playerInfoList:
                        if info.id == client_player_ID:
                            client_player.copy(info)

                    players = []
                    players.append(client_player)

                    for info in playerInfoList:
                        if info.id != client_player_ID:
                            icon_info = submodules.getIcon(info.icon_num)
                            op_posInfo = [info.x, info.y, info.vel_x, info.vel_y]
                            op_hitInfo = [info.hitDisp, info.hit_img_orientation, info.hit_img_center, info.hitList,
                                          info.hitRotAngle, info.hitType]
                            other_player = Player(info.id, info.name, op_posInfo, icon_info[0], info.orientation,
                                                  icon_num,
                                                  op_hitInfo, info.score, info.health, 0, 0, 0, 0)
                            players.append(other_player)

                    events = inits.pygame.event.get()
                    for event in events:
                        if event.type == inits.pygame.QUIT:
                            run = False
                            game_stage = "closing"
                            net.close()
                            break

                        # checking mouse clicks for updating sound buttons & sounds
                        if event.type == inits.pygame.MOUSEBUTTONDOWN:
                            mx, my = inits.pygame.mouse.get_pos()
                            inits.SoundButtons.mouseAction(mx, my)
                            inits.exitGameButton.mouseAction(mx, my)
                            inits.leaveRoomButton.mouseAction(mx, my)
                            if inits.exitGameButton.clicked:
                                net.close()
                                game_stage = "closing"
                                run = False
                            if inits.leaveRoomButton.clicked:
                                net.close()
                                game_stage = "game_over"
                                inits.leaveRoomButton.clicked = False
                                run = False

                        # checking keyboard inputs for hitting
                        if event.type == inits.pygame.KEYDOWN:
                            if event.key == inits.pygame.K_a:
                                hitType = "PUNCH"
                            if event.key == inits.pygame.K_s:
                                hitType = "KICK"
                        if event.type == inits.pygame.KEYUP:
                            if event.key == inits.pygame.K_a:
                                hitBool = 1
                            if event.key == inits.pygame.K_s:
                                hitBool = 1
                            if event.key == inits.pygame.K_w:
                                topScorer = not topScorer
                            if event.key == inits.pygame.K_q:
                                player_condition = not player_condition

                    if hitBool == 0:
                        hitType = "NONE"

                    # updating player location : keyboard input checks are done inside the function
                    client_player.move(settings.MOVE_TIME_WAIT, settings.WIN_DIM, settings.ICON_DIM[0],
                                       settings.ZERO_THR)

                    # check if player gets any potion
                    client_rect = client_player.getPlayerRect()
                    for potion in potionList:
                        potion_rect = inits.health_potion_img.get_rect(topleft=potion[1])
                        getPotion = client_rect.colliderect(potion_rect)
                        if getPotion:
                            obtained_potion_IDs.append(potion[2])
                            if potion[0] == "health":
                                client_player.health = min(client_player.health + 3, inits.playerLog["Health"])
                                hitLoadButton.health_rem = client_player.health
                            if potion[0] == "rapid":
                                start_counter = time.perf_counter()
                                rapid_hit = True

                    if rapid_hit == True:
                        if time.perf_counter() - start_counter > 15:
                            rapid_hit = False
                            client_player.minPunchWait = inits.playerLog["PunchWait"]
                            client_player.minKickWait = inits.playerLog["KickWait"]
                            hitLoadButton.punchWait = inits.playerLog["PunchWait"]
                            hitLoadButton.kickWait = inits.playerLog["KickWait"]
                        else:
                            client_player.minPunchWait = 1
                            client_player.minKickWait = 2
                            hitLoadButton.punchWait = 1
                            hitLoadButton.kickWait = 2

                    # reset the hit list of client player & get the hit_info: (did_player_hit, the Rect object of hitting)
                    client_player.resetHitList()
                    hit_info = client_player.hit(hitType, inits.game_sound_mixer, settings.hit_try_music,
                                                 inits.punch_img, inits.kick_img, settings.ICON_DIM[2],
                                                 settings.ICON_DIM[4], settings.ICON_DIM[0],
                                                 settings.ZERO_THR)
                    if hit_info[0] == "YES":
                        hit_rect = hit_info[1]

                    # update hit load buttons
                    hitLoadButton.lastHitTime = client_player.lastHitTime
                    hitLoadButton.updateHitLoad(time.perf_counter())

                    # update player health if other players hit matches the client ID
                    # update the hit list of the client (other player IDs & damage performed )
                    # based on collision check of client hit Rect & other player icon Rect object
                    for player in players:
                        check_id = player.id
                        if check_id != client_player_ID:
                            # check if the client player is hit by other players & update the health points
                            for hits in player.getHitList():
                                if hits[0] == client_player_ID:
                                    inits.game_sound_mixer.Channel(2).play(
                                        inits.game_sound_mixer.Sound(settings.hit_success_music))
                                    if client_player.health - hits[1] <= 0:
                                        client_player.KO = True
                                        inits.game_sound_mixer.Channel(3).play(
                                            inits.game_sound_mixer.Sound(settings.ko_music))

                                    client_player.health = max(0, client_player.health - hits[1])
                                    hitLoadButton.health_rem = client_player.health

                            # check if the client player manage to hit other players & update the client players hit list & sounds
                            if hit_info[0] == "YES":
                                check_rect = player.getPlayerRect()
                                hit_success = hit_rect.colliderect(check_rect)
                                if hit_success == 1:
                                    inits.game_sound_mixer.Channel(2).play(
                                        inits.game_sound_mixer.Sound(settings.hit_success_music))
                                    client_player.updateHitList(check_id, client_player.getDamage(hitType))
                                    client_player.score += client_player.getDamage(hitType)
                                    if client_player.getDamage(hitType) > player.health:
                                        client_player.KO = True
                                        inits.game_sound_mixer.Channel(3).play(
                                            inits.game_sound_mixer.Sound(settings.ko_music))

                    drawings.draw_stage_play(players, client_player_ID, topScorer, hitLoadButton, potionList,
                                             player_condition)
                    hitType = "NONE"
                    client_player_info = PlayerInfo(client_player, obtained_potion_IDs)

                    # adjust the background and hit sounds
                    routines.sound_set_routine()

    if playerLogChange:
        score = round(client_player_info.score)
        gainCoin = submodules.calculateGold(score)
        inits.playerLog["Coins"] = gainCoin + inits.playerLog["Coins"]
        if score > inits.playerLog["BestScore"]:
            newBestScore = True
            inits.playerLog["BestScore"] = score
        if score > settings.LEVEL_PTS[inits.playerLog["Level"]]:
            inits.playerLog["Level"] += 1
            newLevelGain = True

    output = [game_stage, gainCoin, newBestScore, newLevelGain, score]
    return output

