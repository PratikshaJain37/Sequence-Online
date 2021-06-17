'''
Sequence Online
find_sequence.py - for testing and storing

Author: Pratiksha Jain

'''

import random

# --- --------#
#random grid generator
def randomGrid(choice=[0,1,2]):
    #choice = [0, 1, 2]
    grid = [[4]+random.choices(choice, k=8)+[4] if j==0 or j==9 else random.choices(choice, k=10) for j in range(10)]
    return grid

'''
grid = [
    [4, 0, 2, 2, 1, 2, 1, 0, 2, 4], 
    [3, 0, 3, 3, 1, 0, 0, 1, 0, 0], 
    [2, 2, 2, 0, 3, 2, 0, 0, 3, 3], 
    [3, 1, 0, 2, 1, 1, 2, 1, 0, 2], 
    [2, 3, 1, 3, 1, 0, 2, 0, 1, 1], 
    [0, 0, 3, 1, 3, 2, 1, 0, 2, 0], 
    [1, 2, 1, 1, 2, 1, 1, 2, 0, 3], 
    [0, 0, 2, 3, 0, 1, 0, 1, 1, 0], 
    [2, 1, 1, 3, 2, 1, 0, 2, 2, 1], 
    [4, 1, 0, 1, 2, 0, 1, 3, 3, 4]
    ]
'''
# --- --------#

grid = [
    [4, 1, 2, 2, 0, 0, 0, 1, 2, 4], 
    [2, 0, 1, 0, 1, 1, 1, 1, 1, 0], 
    [2, 1, 1, 2, 0, 1, 2, 1, 2, 2], 
    [1, 1, 0, 1, 1, 0, 1, 2, 0, 2], 
    [1, 2, 0, 1, 0, 1, 1, 1, 0, 2], 
    [0, 1, 0, 0, 2, 0, 2, 1, 1, 0], 
    [1, 1, 0, 2, 0, 2, 1, 2, 2, 1], 
    [2, 2, 2, 0, 1, 0, 0, 2, 0, 0], 
    [2, 1, 0, 0, 1, 2, 0, 0, 2, 1], 
    [4, 1, 1, 2, 2, 2, 2, 2, 2, 4]
    ]



places = [
    ['0-0', 'S-2', 'S-3', 'S-4', 'S-5', 'S-6', 'S-7', 'S-8', 'S-9', '0-0'], 
    ['C-6', 'C-5', 'C-4', 'C-3', 'C-2', 'H-1', 'H-13', 'H-12', 'H-10', 'S-10'],
    ['C-7', 'S-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6', 'D-7', 'H-9', 'S-12'],
    ['C-8', 'S-13', 'C-6', 'C-5', 'C-4', 'C-3', 'C-2', 'D-8', 'H-8', 'S-13'],
    ['C-9', 'S-12', 'C-7', 'H-6', 'H-5', 'H-4', 'H-1', 'D-9', 'H-7', 'S-1'],
    ['C-10', 'S-10', 'C-8', 'H-7', 'H-2', 'H-3', 'H-13', 'D-10', 'H-6', 'D-2'], 
    ['C-12', 'S-9', 'C-9', 'H-8', 'H-9', 'H-10', 'H-12', 'D-12', 'H-5', 'D-3'],
    ['C-13', 'S-8', 'C-10', 'S-12', 'S-13', 'C-1', 'D-1', 'D-13', 'H-4', 'D-4'],
    ['C-1', 'S-7', 'S-6', 'S-5', 'S-4', 'S-3', 'S-2', 'H-2', 'H-3', 'D-5'],
    ['0-0', 'D-1', 'D-13', 'D-12', 'D-10', 'D-9', 'D-8', 'D-7', 'D-6', '0-0'] 
    
]        

#g_2 = graph(2)
#g_1 = graph(2)
#print(g_1.gdict)
#g_1.findSequence()
'''
H-11-2 2-2
S-5-0 0-4
H-11-1 0-4

'''
#g_1.validateSequence()


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


#bo = board(grid, [1,2])
#bo.findAllSequences_n(3)

D = Deck()
D.initialBuild()
D.shuffle()

hands = D.serveHands()

players = [Player('1', 'b'), Player('2', 'r')]

for id, player in enumerate(players):
    player.hand = hands[id]

bo = Board(grid, [0,1])
bo.updateSequences(0)

'''






