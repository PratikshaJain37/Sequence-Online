from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from classes import Game, Room, places

# dictionary of rooms (id: Room)
rooms = {}

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

        if room_id in rooms.keys():
            return redirect(url_for("error", message="Room already exists"))
        if room_id == '' or room_pwd=='':
            render_template("createroom.html")

        rooms[room_id] = Room(room_id, room_pwd)
        
        return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1))

    return render_template("createroom.html")

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


@app.route("/joinroom", methods=["GET",'POST'])
def joinroom():
    global rooms
    if request.method == 'POST':

        room_id = request.form.get('room_id', type=int)
        room_pwd = request.form.get('room_pwd', type=str)

        if roomDoesNotExist(room_id):
            return redirect(url_for("error",message="Room Does Not Exist"))

        if passwordIncorrect(room_id, room_pwd):
            return redirect(url_for("error",message="Wrong Password"))
        
        if isRoomFull(room_id):
            return redirect(url_for("error",message="Room Full"))
        
        rooms[room_id].initiatePlayer()   
        
        return redirect(url_for('waiting_room', id=room_id, player=rooms[room_id].numberOfPlayers()-1))
        
    return render_template("joinroom.html")


@app.route("/room/<int:id>/<int:player>", methods=["GET","POST"])
def waiting_room(id, player):
    global rooms
    if request.method == "POST":
        
        name = request.form.get('name', type=str)
        if name != '':
            rooms[id].activateGame()

            return redirect(url_for('play', id=id, player=player, name=name))
        
    return render_template('room.html', id=id, player=player)

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
    app.run(debug=False, port=5000)