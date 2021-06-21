from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from game2 import Game
from find_sequence import places


#https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/

rooms = {}

class Room():
    def __init__(self,id, password) -> None:
        self.password = password
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






app = Flask(__name__, 
static_url_path='',
static_folder="static",
template_folder="templates",
)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/", methods=["GET",'POST'])
def home():
    global rooms
    if request.method == 'POST':

        value = request.form.get('btn')
        print(value)
        if value == 'create':
            return redirect(url_for('createroom'))
        elif value == 'join':
            return redirect(url_for('joinroom'))
    return render_template("home.html")

@app.route("/createroom", methods=["GET",'POST'])
def createroom():
    global rooms
    if request.method == 'POST':

        room_id = request.form.get('room_id', type=int)

        room_pwd = request.form.get('room_pwd', type=str)

        if room_id in rooms.keys():
            return redirect(url_for("error", message="Room already exists"))
        else:
            rooms[room_id] = Room(room_id, room_pwd)
            return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1))

    return render_template("createroom.html")

@app.route("/joinroom", methods=["GET",'POST'])
def joinroom():
    global rooms
    if request.method == 'POST':

        room_id = request.form.get('room_id', type=int)

        room_pwd = request.form.get('room_pwd', type=str)


        if room_id in rooms.keys():
            if room_pwd == rooms[room_id].password:
                rooms[room_id].initiatePlayer()
                
                return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1))
            
            return redirect(url_for("error",message="Wrong Password"))
        return redirect(url_for("error",message="Room Does Not Exist"))

    return render_template("joinroom.html")


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
            return redirect(url_for('error', message="Room Full"))
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

            card_pos = request.form['cardpos']
            card_id = request.form['cardid']

            move = card_id+' '+card_pos
            status = room.playerMove(player, move)
    
            return render_template('play.html', id=id, player=player, name = name, move=move, status=status, grid=room.game.board.grid, places=places,hand = room.game.players[player].showHand(returnValue=True), players=room.players, moves=room.moves, pwd=room.password)
    
    return render_template('play.html', id=id, player=player, name=name, move=move, grid=room.game.board.grid, places=places, hand = room.game.players[player].showHand(returnValue=True), players=room.players, moves=room.moves, pwd=room.password)

@app.route("/error")
def error():
    message = request.args.get("message")
    return render_template('error.html', message=message)

@app.route("/rules")
def rules():
    return render_template('rules.html')

app.jinja_env.globals.update(zip=zip)

if __name__ == "__main__":
    app.run(debug=False)