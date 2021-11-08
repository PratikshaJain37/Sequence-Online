'''
Sequence Online -- Classes.py: Stores all Classes 

Author: Pratiksha Jain

'''


# classes for pygame

from itertools import product
import random


places = [
        ['0-0', 'S-2', 'S-3', 'S-4', 'S-5', 'S-6', 'S-7', 'S-8', 'S-9', '0-0'], 
        ['C-6', 'C-5', 'C-4', 'C-3', 'C-2', 'H-1', 'H-13', 'H-12', 'H-10', 'S-10'],
        ['C-7', 'S-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6', 'D-7', 'H-9', 'S-12'],
        ['C-8', 'S-13', 'C-6', 'C-5', 'C-4', 'C-3', 'C-2', 'D-8', 'H-8', 'S-13'],
        ['C-9', 'S-12', 'C-7', 'H-6', 'H-5', 'H-4', 'H-1', 'D-9', 'H-7', 'S-1'],
        ['C-10', 'S-10', 'C-8', 'H-7', 'H-2', 'H-3', 'H-13', 'D-10', 'H-6', 'D-2'], 
        ['C-12', 'S-9', 'C-9', 'H-8', 'H-9', 'H-10', 'H-12', 'D-12', 'H-5', 'D-3'],
        ['C-13', 'S-8', 'C-10', 'C-12', 'C-13', 'C-1', 'D-1', 'D-13', 'H-4', 'D-4'],
        ['C-1', 'S-7', 'S-6', 'S-5', 'S-4', 'S-3', 'S-2', 'H-2', 'H-3', 'D-5'],
        ['0-0', 'D-1', 'D-13', 'D-12', 'D-10', 'D-9', 'D-8', 'D-7', 'D-6', '0-0'] 

        ]

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
        self.sequences = {}
        self.move = ''

    def addPlayer(self, player, name):
        if player == 0:
            self.players.append(Player(name, 'b'))
        elif player == 1:
            self.players.append(Player(name, 'r'))
        else:
            self.players.append(Player(name, 'g'))
        self.sequences[player] = []

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


class Room():
    def __init__(self,id, password) -> None:
        self.password = password
        self.active = 0
        self.id = id
        self.game = None
        self.lastplayed = {0:{'Name':'', 'Move':'', 'Status':''}}
    
    def initiatePlayer(self):
        self.lastplayed[self.numberOfPlayers()] = {'Name':'', 'Move':'', 'Status':''}

    def addPlayerName(self, player, name):
        self.lastplayed[player]['Name'] = name

    def numberOfPlayers(self):
        return len(self.lastplayed)
    
    def playerMove(self, player, move):

        self.game.move = move
        card_id, pos = self.game.getMove()
        status = self.game.play(player, card_id, pos)

        if status == 0:
            self.game.updateTurn()

        self.lastplayed[player]['Move'] = move
        self.lastplayed[player]['Status'] = self.statusText(status)
        
        return status
    
    def statusText(self, status):
        status_dict = {
            -1: "Game Over!",
            0: "Accepted",
            1:"One eyed joker trying to remove fixed card",
            2:"no wildcard, Wrong card or location entered",
            3:"space not empty - cannot place card there",
            4:"wildcard(1) used incorrectly: no card present there",
            5:"Not present in cards",
            6: "Not your turn yet"
        }
        return status_dict[status]

    def activateGame(self):

        self.game = Game(self.id)
        for player, dict in self.lastplayed.items():
            self.game.addPlayer(player, dict["Name"])
        self.game.startGame()

        self.active = 1




