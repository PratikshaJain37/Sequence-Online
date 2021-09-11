'''
Sequence Online
playbox.py - for testing and storing

Author: Pratiksha Jain

'''

import random
from classes import Graph

#-------------#

#random grid generator
def randomGrid(choice=[0,1,2]):
    #choice = [0, 1, 2]
    grid = [[4]+random.choices(choice, k=8)+[4] if j==0 or j==9 else random.choices(choice, k=10) for j in range(10)]
    return grid

'''
grid1 = [
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
#-------------#

grid = [
    [4, 1, 2, 2, 0, 0, 0, 1, 2, 4], 
    [2, 0, 1, 0, 1, 1, 1, 1, 1, 0], 
    [2, 1, 1, 2, 0, 1, 2, 1, 2, 2], 
    [1, 1, 0, 1, 1, 0, 1, 2, 0, 2], 
    [1, 2, 0, 1, 0, 1, 1, 1, 0, 2], 
    [0, 1, 0, 0, 2, 2, 2, 1, 1, 2], 
    [1, 1, 0, 2, 0, 2, 2, 2, 2, 2], 
    [2, 2, 2, 0, 1, 0, 0, 2, 0, 2], 
    [2, 1, 0, 0, 1, 2, 0, 0, 2, 2], 
    [4, 1, 1, 0, 0, 2, 2, 2, 2, 4]
    ]    

'''

#------ Checking Sequences are being found correctly -------#
g_2 = Graph(2, grid)
g_1 = Graph(1, grid)

g_2.findSequences()
print(g_2.gdict)
print(g_2.sequences)

H-11-2 2-2
S-5-0 0-4
H-11-1 0-4

'''
