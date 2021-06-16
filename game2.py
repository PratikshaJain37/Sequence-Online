from classes import Board, Player, Deck, Card

class Game():
    def __init__(self, id, players=['prati','anu']):
        self.id = id
        
        
        self.board =  Board([[4]+[-1 for i in range(8)]+[4] if j==0 or j==9 else [-1 for i in range(10)] for j in range(10)])
        
        self.players = [Player(players[0], 'b'), Player(players[1], 'r')]
        self.turn = 0
        self.deck = Deck()

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

        if player == self.turn:
            if self.players[player].validPlay(card_id):
                if self.board.validPlayOnBoard(pos[0], pos[1], card_id):
                    # update board
                    self.board.updateBoard(player, pos[0], pos[1])
                    # update hands
                    self.players[player].removeCard(card_id)
                    self.players[player].addCard(self.deck)
                    
                    # check if winner
                    if self.isWinner(player):
                        return -1

                    else:
                        return 0  
                else:
                    print("Not valid on board")
                    return 1  

            else:   
                print('Not present in cards')
                return 2
        else:
            print("Wrong Player")
            return 2


    def updateTurn(self):
        self.turn = (self.turn+1)%2

    def isWinner(self, player):

        self.board.graphs[player+1].findSequences()
        self.board.sequences[player] = self.board.graphs[player].sequences

        if self.board.sequences[player+1] != []:
            print("Winner: Player ", player)
            return True
        else:
            return False