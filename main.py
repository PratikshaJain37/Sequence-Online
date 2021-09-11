'''
Sequence Online
main.py - main script to run and game loop

Author: Pratiksha Jain

'''

#-------------#
# Imports 

from game import Game

#-------------#

# Initializing Game
p1 = input("Enter player 1 name: ")
p2 = input("Enter player 2 name: ")

game = Game(1, players=[p1, p2])
game.startGame()

print (game.players[0].showHand())
print (game.players[1].showHand())

game.board.showBoard()
run = True
move = ''

#-------------#

# Game Loop

while run:
    player = game.turn
    game.move = input("It is player %s turn:     "%(game.players[player].name))
    card_id, pos = game.getMove()

    status = game.play(player, card_id, pos)

    
    if status == -1: # winner
        run = False
    elif status == 0: # valid turn
        game.players[player].showHand()
        game.updateTurn()
        game.board.showBoard()
           

    elif status == 1:
        print("try again")
        pass
    elif status == 2:
        print("try again")
        pass
    elif status == 3:
        print("try again")
        pass
    elif status == 4:
        print("try again")
        pass
    elif status == 5:
        print("try again")
        pass
    elif status == 6:
        print("try again")
        pass
    
#-------------#     


