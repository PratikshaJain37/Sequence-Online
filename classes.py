# classes for pygame
from itertools import product
from find_sequence import grid

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
                    self.dfs(stack, id2, diff)

    def dfs(self, visited, node, diff):  #function for dfs 
        
        if node not in visited:
            visited.append(node)
            if len(visited) == 5:
                self.sequences.append(visited)
                return True
            
            found = False
            for neighbour in self.gdict[node]:
                if neighbour-node == diff:
                    self.dfs(visited, neighbour, diff)
            return found

    def validateSequence(self):
    
        pass


bo = board(grid, [1,2])
bo.findAllSequences()

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

class card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.type = 0
        # 0 for normal, 1 for 1 eyed joker, 2 for 2 eyed joker


# deck class

class deck():
    def __init__(self):
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

