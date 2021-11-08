

from data import rooms
from classes import Room, Game, Player



def createRoom(room_id, room_pwd):
    global rooms
    rooms[room_id] = Room(room_id, room_pwd)

def startGame(room_id):
    global rooms
    room = rooms[room_id]

    room.activateGame()

    # Game
    room.game = Game(room_id)

    room.game.players.append(Player(room.P0_Name, 'b'))
    room.game.players.append(Player(room.P1_Name, 'r'))

    room.game.startGame()
