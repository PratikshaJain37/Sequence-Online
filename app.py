from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from game2 import Game
from find_sequence import places


#https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/

# dictionary of rooms (id: Room)
rooms = {}

class Room():
    def __init__(self,id, password, maxplayers) -> None:
        self.password = password
        self.active = 0
        self.id = id
        self.game = None
        self.lastplayed = {0:{'Name':'', 'Move':'', 'Status':''}}
        self.maxplayers = maxplayers
    
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




app = Flask(__name__, 
static_url_path='',
static_folder="static",
template_folder="templates",
)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

# Home Page - Button to create room + join room
@app.route("/", methods=["GET",'POST'])
def home():
    if request.method == 'POST':

        value = request.form.get('btn')
        if value == 'create':
            return redirect(url_for('createroom'))
        elif value == 'join':
            return redirect(url_for('joinroom'))
    return render_template("home.html")


# Create Room - 
@app.route("/createroom", methods=["GET",'POST'])
def createroom():
    global rooms
    if request.method == 'POST':

        room_id = request.form.get('room_id', type=int)
        room_pwd = request.form.get('room_pwd', type=str)
        room_maxplayers = request.form.get('room_maxplayers', type=int)

        if room_id in rooms.keys():
            return redirect(url_for("error", message="Room already exists"))
        if room_id == '' or room_pwd=='' or room_maxplayers == '':
            render_template("createroom.html")

        rooms[room_id] = Room(room_id, room_pwd, room_maxplayers)
        
        return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1, maxplayers=room_maxplayers))

    return render_template("createroom.html")

@app.route("/joinroom", methods=["GET",'POST'])
def joinroom():
    global rooms
    if request.method == 'POST':

        room_id = request.form.get('room_id', type=int)
        room_pwd = request.form.get('room_pwd', type=str)


        if not room_id in rooms.keys():
            return redirect(url_for("error",message="Room Does Not Exist"))

        if room_pwd != rooms[room_id].password:
            return redirect(url_for("error",message="Wrong Password"))
        
        if rooms[room_id].numberOfPlayers() == rooms[room_id].maxplayers:
            return redirect(url_for("error",message="Room Full"))
        
        rooms[room_id].initiatePlayer()   
        return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1, maxplayers=rooms[room_id].maxplayers))
        
    return render_template("joinroom.html")


@app.route("/room/<int:id>/<int:player>", methods=["GET","POST"])
def waiting_room(id, player):
    global rooms
    maxplayers = request.form.get('maxplayers')
    if request.method == "POST":
        
        name = request.form.get('name', type=str)
        if name != '':
            rooms[id].activateGame()
            return redirect(url_for('play', id=id, player=player, name=name))
        
    return render_template('room.html', id=id, player=player, maxplayers=maxplayers)

@app.route("/room/<int:id>/play", methods=["POST", "GET"])
def play(id):
    global rooms
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

            # if status == -1, then game over
    
    return render_template('play.html', id=id, player=player, name=name, move=move, grid=room.game.board.grid, places=places, hand = room.game.players[player].showHand(returnValue=True), pwd=room.password, lastplayed=room.lastplayed)

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