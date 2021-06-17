'''
Sequence Online
main.py - main script to run and game loop

Author: Pratiksha Jain

'''
# main.py

from game2 import Game

#p1 = input("Enter p1 name")
#p2 = input("Enter p2 name")

game = Game(1)
game.startGame()

print (game.players[0].showHand())
print (game.players[1].showHand())

game.board.showBoard()
run = True
move = ''


while run:
    player = game.turn
    game.move = input("It is player %s turn:     "%(game.players[player].name))
    card_id, pos = game.getMove()

    status = game.play(player, card_id, pos)

    
    if status == -1: # winner
        run = False
    elif status == 0: # valid turn
        print (game.players[player].showHand())
        game.updateTurn()
        game.board.showBoard()
           

    elif status == 1:
        pass
    elif status == 2:
        pass
    elif status == 3:
        pass
    elif status == 4:
        pass
    elif status == 5:
        pass
    elif status == 6:
        pass
    
     


