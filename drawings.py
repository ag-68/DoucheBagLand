import time
import settings
import inits

def draw_top_scorers(listOfPlayerInfo, client_ID):

    sorted_list = sorted(listOfPlayerInfo, key=lambda info: info.score, reverse=True)
    width = 230
    score_board_loc = (settings.WIN_DIM[0]-width-10, 80)
    size = (width, 20*len(sorted_list)+40)
    score_board = inits.pygame.Surface(size)
    score_board.set_alpha(settings.ALPHA_VAL[0])
    score_board.fill(settings.TOP_SCORER_COLOR[0])
    inits.gameWindow.blit(score_board,score_board_loc)
    font = inits.pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[4])
    display_text = font.render("Top Scorers", 1, settings.TOP_SCORER_COLOR[1])
    display_text.set_alpha(settings.ALPHA_VAL[0])
    inits.gameWindow.blit(display_text, (score_board_loc[0]+10, score_board_loc[1]+2))
    count=1
    font = inits.pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[5])
    for idx, info in enumerate(sorted_list):
        if info.id == client_ID:
            color = settings.TOP_SCORER_COLOR[3]
            alpha = settings.ALPHA_VAL[1]
        else:
            color = settings.TOP_SCORER_COLOR[2
            ]
            alpha = settings.ALPHA_VAL[0]
        display_text = font.render(str(count) + ". " + info.name + ": " + str(int(info.score)), 1, color)
        display_text.set_alpha(alpha)
        inits.gameWindow.blit(display_text, (score_board_loc[0]+3, score_board_loc[1]+count*25))
        count += 1


def draw_frame():
    #pygame.draw.rect(gameWindow, FRAME_COLOR, (0,0,FRAMED_WIN_DIMENSIONS[2],FRAMED_WIN_DIMENSIONS[1]))
    inits.pygame.draw.rect(inits.gameWindow, settings.FRAME_COLOR, (0, 0, settings.WIN_DIM[0], settings.WIN_DIM[2]))
    #pygame.draw.rect(gameWindow, FRAME_COLOR, (0, FRAMED_WIN_DIMENSIONS[1]-FRAMED_WIN_DIMENSIONS[2], FRAMED_WIN_DIMENSIONS[0], FRAMED_WIN_DIMENSIONS[2]))
    #pygame.draw.rect(gameWindow, FRAME_COLOR, (FRAMED_WIN_DIMENSIONS[0]-FRAMED_WIN_DIMENSIONS[2], 0, FRAMED_WIN_DIMENSIONS[2], FRAMED_WIN_DIMENSIONS[1]))

def draw_all():
    inits.gameWindow.fill(settings.GAME_BG_COLOR)
    draw_frame()
    inits.SoundButtons.drawSoundButton(inits.gameWindow, inits.bg_volume_on_img, inits.bg_volume_off_img, inits.hit_volume_on_img, inits.hit_volume_off_img)
    inits.exitGameButton.drawCloseButton(inits.gameWindow)
    fonts = inits.pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[11])
    best_score_text = fonts.render("Best Score: " + str(int(inits.playerLog["BestScore"])), 1, (255, 255, 255))
    level_text = fonts.render("Level: " + settings.LEVEL_NAME[int(inits.playerLog["Level"])], 1, (255, 255, 255))
    inits.gameWindow.blit(level_text, (settings.WIN_DIM[0] - 200, 4))
    inits.gameWindow.blit(best_score_text, (settings.WIN_DIM[0]-200, 26))

def draw_potions(potionList):

    for potion in potionList:
        if potion[0] == "health":
            inits.gameWindow.blit(inits.health_potion_img, potion[1])
        if potion[0] == "rapid":
            inits.gameWindow.blit(inits.rapid_hit_potion_img, potion[1])

def draw_stage_name():
    draw_all()
    if inits.playerLog["Coins"] > 0:
        inits.goToShopButton.drawCloseButton(inits.gameWindow)
    inits.nameButton.drawNameButton(inits.gameWindow, int(settings.WIN_DIM[0]/2)-100, int(settings.WIN_DIM[1]/2)-100)
    inits.gameDisp.update()


def draw_stage_connect():
    draw_all()
    settings.connectButton.drawConnectButton(inits.gameWindow, int(settings.WIN_DIM[0]/2)-100, int(settings.WIN_DIM[1]/2)-100)
    inits.gameDisp.update()

def draw_no_connection():
    draw_all()
    fonts = inits.pygame.font.SysFont(settings.DISP_FONT, 30)
    display_text = fonts.render(str("No Connection to Server..."), 1, (0, 0, 0))
    run = True
    start_time = time.perf_counter()
    while run:
        current_time = time.perf_counter()
        if current_time - start_time > 1.5:
            run = False
        else:
            inits.gameWindow.blit(display_text, (settings.WIN_DIM[0]/2-100, settings.WIN_DIM[1]/2-settings.WIN_DIM[2]))
            inits.gameDisp.update()

def draw_stage_play(players, client_player_ID, topScorer, hit_load_button, potionList, player_condition):
    draw_all()
    inits.leaveRoomButton.drawCloseButton(inits.gameWindow)

    draw_potions(potionList)
    for player in players:
        player.drawPlayer(inits.gameWindow, settings.ICON_DIM[0])
        if player.id == client_player_ID:
            player.drawPointer(inits.gameWindow, settings.ICON_DIM[0], settings.POINTER_FEATURES, settings.ZERO_THR)

    for player in players:
        player.drawHit(inits.gameWindow, inits.punch_img, inits.kick_img, settings.ICON_DIM[0], settings.ICON_DIM[2], settings.ICON_DIM[4], settings.ZERO_THR)

    if topScorer:
        draw_top_scorers(players, client_player_ID)
    if player_condition:
        hit_load_button.drawHitLoad(inits.gameWindow, settings.WIN_DIM[0]-100, settings.WIN_DIM[1]-100)
    inits.gameDisp.update()

def draw_stage_shop(shopButtonList):
    draw_all()
    inits.backButton.drawCloseButton(inits.gameWindow)
    fonts = inits.pygame.font.SysFont(settings.DISP_FONT, settings.FONT_SIZE[8])
    rem_coin_text = fonts.render("Remaining Coins: "+str(int(inits.playerLog["Coins"])), 1, settings.SHOP_COLOR[0])
    inits.gameWindow.blit(rem_coin_text, (10, settings.WIN_DIM[2]+30))
    img_offset =  (settings.RECT_DIM[5]-settings.RECT_DIM[6])/2
    for idx,sb in enumerate(shopButtonList):
        sb.drawButton(inits.gameWindow)
        if idx == 0:
            img = inits.health_shop_img
        elif idx == 1:
            img = inits.hit_speed_shop_img
        else:
            img = inits.hit_damage_shop_img
        img.set_alpha(sb.alpha)
        inits.gameWindow.blit(img, (sb.x+img_offset, sb.y+img_offset))


    for idx,sb in enumerate(shopButtonList):
        if sb.clicked:
            if idx == 0:
                img = inits.health_shop_img
            elif idx == 1:
                img = inits.hit_speed_shop_img
            else:
                img = inits.hit_damage_shop_img
            img.set_alpha(sb.alpha)
            inits.gameWindow.blit(img, (sb.x+img_offset, sb.y+img_offset))
            sb.drawClickedButton(inits.gameWindow)


    inits.gameDisp.update()


