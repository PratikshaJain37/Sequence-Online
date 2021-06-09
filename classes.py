# classes for pygame

# player class
class player():
    def __init__(self,id, name, color) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.enable = False
        self.cards = []
    
    def toggleEnable(self):
        if self.enable == False:
            self.enable = True
        else:
            self.enable = False
    
    def takeCard(self, card):
        self.cards = self.cards.append(card)
        
    def removeCard(self, card):
        self.cards = self.cards.remove(card)



# players list
class players():
    def __init__(self) -> None:
        self.playerList = []
        self.playerOrder = {}
        self.teams = []
    
    def addPlayer(self, player):
        self.playerList = self.playerList.append(player)
        # assign to team abhi, or later?

    def removePlayer(self):
        pass

    def generateOrder(self):
        pass

    def changeTurn(self):
        pass


# board class
class board():
    def __init__(self) -> None:
        self.grid = [[0 for i in range(10)] for j in range (10)]
        self.places = []
    
    def findSequence():
        pass

    def updateBoard():
        pass


# place class
class place():

    def __init__(self, row, column, rank, suit) -> None:
        self.row = row
        self.column = column
        self.position = (row,column)
        self.rank = rank
        self.suit = suit
        self.card = (rank, suit)
        self.color = 'white'
        self.fixed = False

    def fillPlace():
        pass

    def fixPlace():
        pass

    def validMatch():
        pass



# card class

def card():
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit
        self.type = 0
        # 0 for normal, 1 for 1 eyed joker, 2 for 2 eyed joker


# deck class

def deck():
    def __init__(self) -> None:
        self.unused = [card(rank, suit) for rank in [1,2,3,4,5,6,7,8,9,10,11,12,13] for suit in ["H","D","S","C"]] # all cards here
        self.used = []

    def distributeCards(self):
        pass
    
    def shuffleDeck(self):
        pass

    def useCard():
        
        pass

    def updateDeck(self):
        if self.unused == []:
            self.unused = self.used
