'''
Sequence Online
classes.py - stores all classes and uses

Author: Pratiksha Jain

'''


# classes for pygame

from itertools import product
#from find_sequence import places
import random

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
    
    def showHand(self, returnValue=False):
        hands = []
        for card in self.hand:
            hands.append(card.id)
        if returnValue:
            return hands
        print(hands)
            


# board class
class Board():
    def __init__(self, grid, players=[0,1]) -> None:
        self.grid = grid
        self.places = {}
        self.graphs = [Graph(i, grid) for i in players]

        ##
        #self.sequences = {i:[] for i in players}
        ##

        # generating places
        for i in range(10):
            for j in range(10):
                suit,val = places[i][j].split('-')
                if (i,j) in [(0,0), (0,9), (9,0), (9,9)]:
                    self.places[(i,j)] = Place(suit, val, i,j, 4,1)

                
                # filled=-1,0,1,2,3,4 fixed=1
                self.places[(i,j)] = Place(suit, val, i,j, -1,0)

  
    def validPlayOnBoard(self, x,y, card_id):
        if self.places[(x,y)].card.id == card_id:
            return True
        else:
            return False
    
    def spaceEmpty(self, x,y):
        if self.places[(x,y)].filled == -1:
                return True
        else:
            return False

    def updateBoard(self, player, x,y,card_id):
        wildcard = int(card_id.split("-")[2])
        if wildcard == 0: # not wild card
            self.places[(x,y)].filled = player
            self.grid[x][y] = player
        
        elif wildcard == 1: # one eyed - removes
            self.places[(x,y)].filled = -1 
            self.grid[x][y] = -1
        
        elif wildcard == 2: # two-eyed - adds
            self.places[(x,y)].filled = player 
            self.grid[x][y] = player

    
    def showBoard(self):
        print("Grid:")
        for row in self.grid:
            print(row)
        
class Place():
    def __init__(self, suit, val, x, y, filled, fixed) -> None:
        self.card = Card(suit, val)
        self.suit = suit
        self.val = val
        self.filled = filled
        self.fixed = fixed
        self.x = x
        self.y = y
    
    def fixPlace(self):
        self.fixed = 1
            

# graph class for doing sequences
class Graph():
    def __init__(self, color, grid):
        self.grid = grid
        self.gdict = {}
        self.color = color

        for id in range(100):
            row = id//10
            col = id%10
            if self.grid[row][col] in (self.color, 4):
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
            if self.grid[r][c] in (self.color, 4):
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
    




# card class
class Card():
    def __init__(self, suit, val, wild=0) -> None:
        # id is a string which is of the form "S-14-0" {suit, value, wild}

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
        random.Random(4).shuffle(self.cards)
        
    def drawCard(self):
        return self.cards.pop(0)

    def serveHands(self, numberofplayers=2, numberofcards=7):
        mat = [[0 for i in range(numberofcards)] for j in range(numberofplayers)]
        for j in range(numberofcards):
            for i in range(numberofplayers):
                mat[i][j] = self.drawCard()
        
        return mat



