'''
Sequence Online
game2.py - script with game class

Author: Pratiksha Jain

'''


from classes import Board, Player, Deck, Card

class Game():
    def __init__(self, id, players=['prati','anu']):
        self.id = id
        
        
        self.board =  Board([[4]+[-1 for i in range(8)]+[4] if j==0 or j==9 else [-1 for i in range(10)] for j in range(10)])
        
        self.players = [Player(players[0], 'b'), Player(players[1], 'r')]
        self.turn = 0
        self.deck = Deck()

        self.sequences = {i:[] for i in range(len(players))}

        self.move = ''

    def startGame(self):
        self.deck.initialBuild()
        self.deck.shuffle()

        hands = self.deck.serveHands()
        
        for id, player in enumerate(self.players):
            player.hand = hands[id]

    def getMove(self):
        # str -> list
        # H-1-0 9-10
        card_id, pos = self.move.split()
        card_id = card_id.upper()
        pos = tuple(map(int, pos.split("-")))
        return card_id, pos

   
    def play(self, player, card_id, pos):
        wildcard = int(card_id.split("-")[2])
        if player != self.turn: # not players turns
            return 6
        elif not (self.players[player].validPlay(card_id)):
            print('Not present in cards') # card played is not in hand
            return 5
        
        elif wildcard==1 and self.board.spaceEmpty(pos[0], pos[1]) : # one eyed joker trying to remove empty space
            print("wildcard(1) used incorrectly: no card present there")
            return 4
        elif wildcard != 1 and not(self.board.spaceEmpty(pos[0], pos[1])) : # trying to place card in non empty location
            print("space not empty - cannot place card there")
            return 3

        elif wildcard == 0 and not(self.board.validPlayOnBoard(pos[0], pos[1],card_id)): # trying to play card in wrong location (change location)
            print("no wildcard, Wrong card or location entered, ")
            return 2
        
        elif wildcard == 1 and self.board.places[(pos[0], pos[1])].fixed == 1: # one eyed joker trying to remove fixed card
            print("One eyed joker trying to remove fixed card")
            return 1
        
        else:
            self.board.updateBoard(player, pos[0], pos[1], card_id)
            self.players[player].removeCard(card_id)
            self.players[player].addCard(self.deck)
            
            self.updateSequenceFormed(player)

            # check if winner
            if self.isGameOver():
                print("Game Over")
                return -1
            else:
                print("Accepted")
                return 0 


    def updateTurn(self):
        self.turn = (self.turn+1)%len((self.players))

    def updateSequenceFormed(self, player):

        self.board.graphs[player].findSequences()
        self.sequences[player] = self.board.graphs[player].sequences

        # update fixed
        for i in self.sequences[player]:
            for id in i:
                x = id//10
                y = id%10

                self.board.places[(x,y)].fixPlace()


    
    def isGameOver(self):
        for i in range(2):
            if len(self.sequences[i]) == 2:
                print("winner is %s" %(i))
                return True
        else:
            False
