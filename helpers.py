'''
Sequence Online -- helpers.py: helper functions 

Author: Pratiksha Jain

'''

from data import rooms, status_dict

# Validation/Checking for Room
def roomDoesNotExist(room_id):
    global rooms
    if room_id in rooms.keys():
        return False
    return True

def isRoomFull(room_id):
    global rooms
    if rooms[room_id].numberOfPlayers() == 2:
        return True
    return False

def passwordIncorrect(room_id, room_pwd):
    global rooms
    if room_pwd != rooms[room_id].password:
        return True
    return False

def isRoomActive(room_id):
    if rooms[room_id].active == 1:
        return True
    else:
        return False

# Updating

def addPlayerToRoom(room_id):
    global rooms
    rooms[room_id].players += 1

def addPlayerName(room_id, name, player):
    global rooms

    room = rooms[room_id]
    if player == 0:
        room.P0_Name = name
    else:
        room.P1_Name = name


def playMove(room_id, player, move):
    global rooms

    room = rooms[room_id]
    status = room.game.playerMove(player, move)
    if player == 0:
        room.P0_Move = move
        room.P0_Status = parseStatus(status)
    else:
        room.P1_Move = move
        room.P1_Status = parseStatus(status)
        



# Parsing

def parseStatus(status):
    return status_dict[status]
