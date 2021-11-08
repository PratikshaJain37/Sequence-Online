'''
Sequence Online -- dlasses.py: Stores all Classes 

Author: Pratiksha Jain

'''


# classes for pygame

from itertools import product
import random
from data import places
from helpers import parseStatus

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
                break

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
        global places
        self.grid = grid
        self.places = {}
        self.graphs = [Graph(i, grid) for i in players]

                

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
                    if s == "C" or s == "D":
                        self.cards.append(Card(s,v,wild=2))
                    else:
                        self.cards.append(Card(s,v,wild=1))
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



class Game():
    def __init__(self, id):
        self.id = id
        self.board =  Board([[4]+[-1 for i in range(8)]+[4] if j==0 or j==9 else [-1 for i in range(10)] for j in range(10)])
        self.players = []
        self.turn = 0
        self.deck = Deck()
        self.sequences = {0:[], 1:[]}
        self.move = ''
        self.moves = []        

    def startGame(self):
        self.deck.initialBuild()
        self.deck.shuffle()

        hands = self.deck.serveHands()
        
        for id, player in enumerate(self.players):
            player.hand = hands[id]

    def getMove(self):#self.lastplayed[player]['Move'] = move
        #self.lastplayed[player]['Status'] = self.statusText(status)
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
            self.moves.append(str(player)+'- '+self.move)

            # check if winner
            if self.isGameOver():
                print("Game Over")
                return -1
            else:
                print("Accepted")
                return 0 

    def playerMove(self, player, move):
        self.move = move
        card_id, pos = self.getMove()
        status = self.play(player, card_id, pos)

        if status == 0:
            self.updateTurn()
        
        return status

    def getLastMove(self):
        return self.moves[-1]


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


class Room():
    def __init__(self,id, password) -> None:
        self.password = password
        self.active = 0
        self.id = id
        self.game = None
        self.players = 1
        
    def numberOfPlayers(self):
        return self.players
        
    def getLastPlayed(self):
        lastplayed = {}
        lastplayed[0] = {'Name':self.P0_Name, 'Move':self.P0_Move, 'Status':self.P0_Status}
        lastplayed[1] = {'Name':self.P1_Name, 'Move':self.P1_Move, 'Status':self.P1_Status}

        return lastplayed

    def activateGame(self):

        self.P0_Move = ''
        self.P0_Status = ''

        self.P1_Move = ''
        self.P1_Status = ''

        self.active = 1
   
    def deactivateGame(self):
        self.game = None
        self.active = 0




