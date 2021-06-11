# classes for pygame
from itertools import product
from find_sequence import grid
from pydealer import Card, Deck, Stack
#https://pydealer.readthedocs.io/en/latest/usage.html

# player class
class player():
    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color #team
        self.turn = False # if its their turn
        self.cards = [] #assigned cards in hand
    
    def toggleEnable(self):
        if self.turn == False:
            self.turn = True
        else:
            self.turn = False
    
    def takeCard(self, card):
        self.cards = self.cards.append(card)



# players list
class players():
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


bo = board(grid, [1,2])
bo.findAllSequences_n(3)

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

