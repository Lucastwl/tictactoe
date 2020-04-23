from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from tic import *

app = Flask(__name__)
socketio = SocketIO(app)

bored = Train()
episodes = 0

@app.route("/")
def index():

    board = bored.niceBoard()

    return render_template("index.html",board=board, episodes=episodes)

@app.route("/reset",methods=["POST"])
def reset():

    bored.reset()

    return redirect(url_for('index',episodes=episodes))


@app.route("/train",methods=["POST"])
def train():

    global episodes
    bored.reset()
    number = request.form.get('range')
    bored.start(int(number))
    bored.reset()
    episodes = int(number)

    return redirect(url_for('index', episodes=episodes))


@socketio.on("change")
def change(tup):

    bored.set(tup['learn'], tup['disc'])
    board = bored.niceBoard()
    emit("new state", (board, "Applied", []))


@socketio.on("start")
def start():

    bored.agentMove()
    board = bored.niceBoard()
    message = 'cont'
    bored.next()

    emit("new state", (board, message, []))

qvalues = []

@socketio.on("input move")
def input(move):

    selection = move["move"]
    token = np.unravel_index(int(selection),(3,3))

    if bored.addToken(token[0],token[1]) == "bad": # add token and check if it is a valid input
        return emit("invalid")

    board = bored.niceBoard()
    end, message = bored.getMessage()

    if end == True:
        return emit("new state", (board, message, []))

    bored.next()
    qvalues = bored.agentMove()
    board = bored.niceBoard()
    end, message = bored.getMessage()

    if end == True:
        return emit("new state", (board, message, qvalues))

    bored.next()

    emit("new state", (board, message, qvalues))


if __name__ == '__main__':
    socketio.run(app)
