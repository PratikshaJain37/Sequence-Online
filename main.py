#https://www.techwithtim.net/tutorials/python-online-game-tutorial/client/

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

x = 0
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
           

    elif status == 1:
        pass
    elif status == 2:
        pass
    elif status == 3:
        pass
    
    game.board.showBoard() 
    x += 1

    if x == 6:
        break
