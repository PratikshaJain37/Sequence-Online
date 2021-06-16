# classes for pygame

import pygame
from itertools import product
from find_sequence import grid
import random
#https://pydealer.readthedocs.io/en/latest/usage.html

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False




# player class
class Player():
    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color #team
        self.turn = False # if its their turn
        self.hand = [] #assigned cards in hand
    
    def toggleEnable(self):
        if self.turn == False:
            self.turn = True
        else:
            self.turn = False
    
    def drawCard(self, deck):
        self.hand.append(deck.drawCard())
    
    def showHand(self):
        for card in self.hand:
            print(card.id, end=' ')



# players list
class Players():
    def __init__(self) -> None:
        self.playerList = [] # list of <player> objects
        self.playerOrder = []  # the order of turns
        self.teams = {1:[], 2:[], 3:[]} # dict of ids
    
    def addPlayer(self, player, team):
        self.playerList.append(player.name)
        self.teams[team].append(player.name)

    def removePlayer(self):
        pass

    def generateOrder(self):
        for j in len(self.teams[1]):
            for i in self.teams.keys():
                try:
                    self.playerOrder.append(self.teams[i][j])
                except:
                    pass

    def changeTurn(self):
        pass




# board class
class board():
    def __init__(self, grid, colors) -> None:
        self.grid = grid
        self.places = []
        self.colors = colors
        self.graphs = [graph(i) for i in colors]
        self.sequences = {}
    
    def findAllSequences(self):
        for i in self.colors:
            self.graphs[i-1].findSequences()
            self.sequences[i] = self.graphs[i-1].sequences

        print(self.sequences)

    def findAllSequences_n(self, n):
        for i in self.colors:
            self.graphs[i-1].findSequences_n(n)
            self.sequences[i] = self.graphs[i-1].sequences

        print(self.sequences)




    def updateBoard():
        pass

# graph class for doing sequences
class graph():
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




# place class
class Place():

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
class Card:
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

    def addCard():
        pass

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

players[0].showHand()