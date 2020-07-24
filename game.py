
class Game():
    def __init__(self, game_ID, playerInfoList, max_roomplayers):
        self.game_ID = game_ID
        self.currentNumPlayers = 0
        self.free_IDs = list(range(max_roomplayers))
        self.playerInfoList = playerInfoList
        self.potionList = []
        self.free_potion_IDs=[]
        self.canCloseFlg = False


    def removePlayer(self, player_ID):

        # remove from info list
        for idx, info in enumerate(self.playerInfoList):
            if info.id == player_ID:
                self.playerInfoList.pop(idx)
        # add to free id list
        self.free_IDs.append(player_ID)

        self.currentNumPlayers -= 1

    def addPlayer(self, player_info):

        # add to info list
        self.playerInfoList.append(player_info)
        # remove from free id list
        for idx, ids in enumerate(self.free_IDs):
            if  player_info.id == ids:
                self.free_IDs.pop(idx)

        self.currentNumPlayers += 1
