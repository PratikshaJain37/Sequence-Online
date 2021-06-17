from flask import Flask, render_template, request, redirect, url_for

from game2 import Game
from find_sequence import places

rooms = {}

class Room():
    def __init__(self,id) -> None:
        self.active = 1
        self.id = id
        self.game = Game(id)
        self.game.startGame()
        self.players = {0:''}
        self.moves = {0:''}
    
    def initiatePlayer(self):
        self.players[self.numberOfPlayers()] = ''
        self.moves[self.numberOfPlayers()] = ''

    def addPlayerName(self, player, name):
        self.players[player] = name

    def numberOfPlayers(self):
        return len(self.players)
    
    def playerMove(self, player, move):
        self.moves[player] = move

        self.game.move = move
        card_id, pos = self.game.getMove()
        status = self.game.play(player, card_id, pos)

        if status == 0:
            self.game.updateTurn()
            #self.game.players[player].showHand()
            #self.game.board.showBoard()

        return status






app = Flask(__name__)

@app.route("/", methods=["GET",'POST'])
def home():
    global rooms
    if request.method == 'POST':

        room_id = request.form.get('room_id', type=int)

        if room_id in rooms.keys():
            print()
            rooms[room_id].initiatePlayer()
        else:
            rooms[room_id] = Room(id)

        return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1))

    return render_template("home.html")

@app.route("/room/<int:id>/<int:player>", methods=["GET","POST"])
def waiting_room(id, player):
    if request.method == "POST":
        try:
            name = request.form.get('name', type=str)

            return redirect(url_for('play', id=id, player=player, name=name))
        except:
            # in case no name mentioned
            pass

    # enter names - once 2 names are there, you can go to play
    else:
        if player>2:
            # invalid room/room full
            return redirect(url_for('home'))
        else:
            return render_template('room.html', id=id, player=player)

@app.route("/room/<int:id>/play", methods=["POST", "GET"])
def play(id):
    # base case
    room = rooms[id]
    player = int(request.args.get("player"))
    name = request.args.get("name")
    move=''
    if room.active == 1:
        if request.method == "POST":

            move = request.form.get('move', type=str)
            
            status = room.playerMove(player, move)
    
            return render_template('play.html', id=id, player=player, name = name, move=move, status=status, grid=room.game.board.grid, places=places,hand = room.game.players[player].showHand(returnValue=True), players=room.players, moves=room.moves)
    
    return render_template('play.html', id=id, player=player, name=name, move=move, grid=room.game.board.grid, places=places, hand = room.game.players[player].showHand(returnValue=True), players=room.players, moves=room.moves)


@app.route("/rules")
def rules():
    return render_template('rules.html')

app.jinja_env.globals.update(zip=zip)

if __name__ == "__main__":
    app.run(debug=True)