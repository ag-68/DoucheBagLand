
import game_stage_welcome
import game_stage_name
import game_stage_playDBL
import game_stage_game_over
import game_stage_shop
import inits
import pkg_resources.py2_warn



if __name__ == '__main__':

    # initialize the game stage: g1: type-select -> g2: name-select -> g3: connect & play -> g1 """
    game_stage = "welcome"

    # initialize game application
    playerLogChange = False
    run_game_app = True

    while run_game_app:

        if game_stage == "welcome":
            game_stage = game_stage_welcome.run_game_stage_welcome()
        elif game_stage == "name":
            game_stage = game_stage_name.run_game_stage_name()
        elif game_stage == "play":
            game_info = game_stage_playDBL.run_game_stage_play()
            game_stage = game_info[0]
            gainCoin = game_info[1]
            newBestScore = game_info[2]
            newLevel = game_info[3]
            score = game_info[4]
        elif game_stage == "game_over":
            game_stage = game_stage_game_over.run_game_stage_game_over(gainCoin, newBestScore, newLevel, score)
        elif game_stage == "shop":
            game_stage = game_stage_shop.run_game_stage_shop()
        elif game_stage == "closing":
            inits.newLog.writeFile()
            run_game_app = False

