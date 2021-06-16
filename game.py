from classes import Button

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

        # basically cards/hands
        self.btns = [[Button("H-1-0", 50, 500, (0,0,0)), Button("S-2-0", 250, 500, (255,0,0)), Button("H-3-0", 450, 500, (0,255,0))], [Button("H-1-0", 50, 500, (0,0,0)), Button("H-2-0", 250, 500, (255,0,0)), Button("H-4-0", 450, 500, (0,255,0))]]

    def get_player_move(self, p):
        """
        :param p: [id1,id2]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        self.btns[player] = self.removeButton(player,move)
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0]
        p2 = self.moves[1]

        winner = -1
        # run code for checking winner here, maybe

        if p1 == "H-1-0" and p2 == "H-1-0":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False

    
    def playerButtons(self, player):
        return self.btns[player]
    
    def removeButton(self, player, btnid):
        btns = self.btns[player].copy()
        for id, i in enumerate(self.btns[player]):
            if i.text == btnid:
                btns.pop(id)
                btns.append(Button("H-1-0", 50, 500, (0,0,0)))
                
                break
        #print(self.btns[player])
        return btns
    
    def setButtons(self):
        self.btns = [[Button("H-1-0", 50, 500, (0,0,0)), Button("S-2-0", 250, 500, (255,0,0)), Button("H-3-0", 450, 500, (0,255,0))], [Button("H-1-0", 50, 500, (0,0,0)), Button("H-2-0", 250, 500, (255,0,0)), Button("H-4-0", 450, 500, (0,255,0))]]