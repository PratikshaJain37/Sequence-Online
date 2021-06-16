# classes for pygame

from itertools import product
from find_sequence import grid, places
import random
#https://pydealer.readthedocs.io/en/latest/usage.html

# player class
class Player():
    def __init__(self, name, color) -> None:
        self.id = id # id of player
        self.name = name # name of player - string
        self.hand = [] # assigned cards in hand
        self.color = color # assigned team
    
    def addCard(self, deck):
        self.hand.append(deck.drawCard())
    
    def removeCard(self, card_id):
        for index, card in enumerate(self.hand):
            if card.id == card_id:
                self.hand.pop(index)

    def validPlay(self, card_id):
        for card in self.hand:
            if card.id == card_id:
                return True
        else:
            return False
    
    def showHand(self):
        hands = []
        for card in self.hand:
            hands.append(card.id)
        print(hands)
            




# board class
class Board():
    def __init__(self, grid, players=[0,1]) -> None:
        self.grid = grid
        self.places = {}
        self.graphs = [Graph(i) for i in players]
        self.sequences = {i:[] for i in players}

        # generating places
        for i in range(10):
            for j in range(10):
                suit,val = places[i][j].split('-')
                self.places[(i,j)] = Card(suit, val)
  
    def validPlayOnBoard(self, x,y, card_id):

        # validate if card.id = places.card.id
        if self.places[(x,y)].id == card_id:
            return True
        else:
            return False


    def updateBoard(self, player, x,y):
        self.grid[x][y] = player
        

    def showBoard(self):
        print("Grid:")
        for row in self.grid:
            print(row)
        



        

# graph class for doing sequences
class Graph():
    def __init__(self, color):
        self.gdict = {}
        self.color = color

        for id in range(100):
            row = id//10
            col = id%10
            if grid[row][col] in (self.color, 4):
                self.addColoredEdge(row,col)
        
        self.sequences = []

    def addVertex(self, v):
       if v not in self.gdict:
            self.gdict[v] = []

    def addEdge(self, edge):
        (v1, v2) = tuple(edge)

        if not v1 in self.gdict:
            self.addVertex(v1)
        self.gdict[v1].append(v2)

        if not v2 in self.gdict:
            self.addVertex(v2)
        self.gdict[v2].append(v1)

        self.gdict[v1] = list(set(self.gdict[v1]))
        self.gdict[v2] = list(set(self.gdict[v2]))

    def addColoredEdge(self, row, col):
        neigbours = self.generateNeighbours(row,col)
        
        for r,c in neigbours:
            if grid[r][c] in (self.color, 4):
                self.addEdge((row*10 +col,r*10+c))

    def generateNeighbours(self,row, col):

        neighbours= []
        for c in product(*(range(n-1, n+2) for n in (row,col))):
            if c != (row,col) and all(0 <= n < 10 for n in c):
                neighbours.append(c)
        return neighbours
        
    def findSequences(self):

        for id1 in self.gdict.keys():
            for id2 in self.gdict[id1]:
                stack = [id1]
                if id2>id1:
                    diff = id2-id1
                    self.dfs(stack, id2, diff,5)

    def dfs(self, visited, node, diff, n):  #function for dfs 
        
        if node not in visited:
            visited.append(node)
            if len(visited) == n:
                self.sequences.append(visited)
                return True
            
            found = False
            for neighbour in self.gdict[node]:
                if neighbour-node == diff:
                    self.dfs(visited, neighbour, diff,n)
            return found

    def findSequences_n(self, n): # n>=3
        for id1 in self.gdict.keys():
            for id2 in self.gdict[id1]:
                stack = [id1]
                if id2>id1:
                    diff = id2-id1
                    self.dfs(stack, id2, diff, n)

    def validateSequence(self):
    
        pass




# card class
class Card():
    def __init__(self, suit, val, wild=0) -> None:
        # id is a string which is of the form "0-S-14" {0/1, suit, value}

        self.suit = suit
        self.val = val
        self.wild = wild
        self.id = str(suit)+"-"+str(val)+"-"+str(wild)

class Deck():
    def __init__(self) -> None:
        self.cards = []
    

    def initialBuild(self):
        for s in ['S',"C","D","H"]:
            for v in range(1,14):
                if v == 11:
                    self.cards.append(Card(s,v,wild=1))
                    self.cards.append(Card(s,v,wild=2))
                else:
                    self.cards.append(Card(s,v))
                    self.cards.append(Card(s,v))
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def drawCard(self):
        return self.cards.pop(0)

    def serveHands(self, numberofplayers=2, numberofcards=7):
        mat = [[0 for i in range(numberofcards)] for j in range(numberofplayers)]
        for j in range(numberofcards):
            for i in range(numberofplayers):
                mat[i][j] = self.drawCard()
        
        return mat

'''
D = Deck()
D.initialBuild()
print(D.cards[0].unique)
D.shuffle()
print(D.cards[0].unique)
print(len(D.cards))
hands = D.serveHands()
print(hands[0][6].unique)
print(len(D.cards))

'''
#bo = board(grid, [1,2])
#bo.findAllSequences_n(3)

D = Deck()
D.initialBuild()
D.shuffle()

hands = D.serveHands()

players = [Player('1', 'b'), Player('2', 'r')]

for id, player in enumerate(players):
    player.hand = hands[id]

