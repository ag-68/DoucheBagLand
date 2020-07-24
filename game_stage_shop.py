import settings
import submodules
import drawings
import pygame
import inits
import routines

def run_game_stage_shop():

    # updating the shop costs
    inits.health_shop_button.cost = submodules.calcHealthUpg()
    inits.hit_speed_shop_button.cost = submodules.calcHitSpeedUpg()
    inits.damage_shop_button.cost = submodules.calcDamageUpg()

    # setting the alpha values to indicate availability of purchase
    shopButtons = [inits.health_shop_button, inits.hit_speed_shop_button, inits.damage_shop_button]
    for sb in shopButtons:
        if inits.playerLog["Coins"] >= sb.cost:
            inits.health_shop_button.alpha = settings.ALPHA_VAL[5]

    shop = True
    while shop:
        purchase = False

        # update display dimensions
        submodules.update_display_dimensions(inits.gameDisp)

        # draw shop screen
        drawings.draw_stage_shop(shopButtons)

        # activate shop item when hoover
        mx, my = pygame.mouse.get_pos()
        for sb in shopButtons:
            if inits.playerLog["Coins"] < sb.cost:
                sb.alpha = settings.ALPHA_VAL[4]
            touch = sb.mouseHoover(mx, my)
            if touch:
                if inits.playerLog["Coins"] >= sb.cost:
                    sb.alpha = settings.ALPHA_VAL[6]
            elif not touch:
                if inits.playerLog["Coins"] >= sb.cost:
                    sb.alpha = settings.ALPHA_VAL[5]

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                shop = False
                game_stage = "closing"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                inits.exitGameButton.mouseAction(mx, my)
                inits.backButton.mouseAction(mx, my)
                inits.SoundButtons.mouseAction(mx, my)
                if inits.exitGameButton.clicked:
                    game_stage = "closing"
                    shop = False
                if inits.backButton.clicked:
                    game_stage = "name"
                    inits.backButton.clicked = False
                    shop = False

                if shop:
                    for sb in shopButtons:
                        sb.mouseAction(mx, my)
                        inits.SoundButtons.mouseAction(mx, my)

                        if sb.clicked:
                            if inits.playerLog["Coins"] >= sb.cost:
                                purchase = True

                            while purchase and shop:
                                sb.alpha = settings.ALPHA_VAL[6]
                                events = pygame.event.get()
                                for event in events:
                                    if event.type == pygame.QUIT:
                                        shop = False
                                        purchase = False
                                        game_stage = "closing"

                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        inits.exitGameButton.mouseAction(mx, my)
                                        if inits.exitGameButton.clicked:
                                            game_stage = "closing"
                                            purchase = False
                                            shop = False

                                    if purchase and shop:
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_y or event.key == pygame.K_RETURN:
                                                purchase = False
                                                inits.playerLog["Coins"] = int(inits.playerLog["Coins"] - sb.cost)
                                                if sb.type == "health":
                                                    inits.playerLog["Health"] = round(1.05 * inits.playerLog["Health"],2)
                                                    inits.playerLog["HealthUp"] += 1
                                                    inits.health_shop_button.cost = submodules.calcHealthUpg()
                                                elif sb.type == "hit_speed":
                                                    inits.playerLog["PunchWait"] = round(max(0.95 * inits.playerLog["PunchWait"], 0.75),2)
                                                    inits.playerLog["KickWait"] = round(max(0.95 * inits.playerLog["KickWait"], 0.75),2)
                                                    inits.playerLog["HitSpeedUp"] += 1
                                                    inits.hit_speed_shop_button.cost = submodules.calcHitSpeedUpg()
                                                elif sb.type == "damage":
                                                    inits.playerLog["PunchDamage"] = round(1.05 * inits.playerLog["PunchDamage"], 2)
                                                    inits.playerLog["KickDamage"] = round(1.05 * inits.playerLog["KickDamage"], 2)
                                                    inits.playerLog["HitDamageUp"] += 1
                                                    inits.damage_shop_button.cost = submodules.calcDamageUpg()
                                            elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                                                purchase = False
                                # adjust the background and hit sounds
                                routines.sound_set_routine()

                                # draw shop screen
                                drawings.draw_stage_shop(shopButtons)

                            sb.alpha = settings.ALPHA_VAL[4]
                            sb.clicked = False
        # adjust the background and hit sounds
        routines.sound_set_routine()

    return game_stage





