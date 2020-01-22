from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from tic import *

app = Flask(__name__)
socketio = SocketIO(app)

bored = Train()

@app.route("/")
def index():

    board = bored.niceBoard()

    return render_template("index.html",board=board)

@app.route("/reset",methods=["POST"])
def reset():

    bored.reset()

    return redirect(url_for('index'))


@app.route("/train",methods=["POST"])
def train():

    bored.reset()
    bored.start()
    bored.reset()

    return redirect(url_for('index'))

@socketio.on("start")
def start():

    bored.agentMove()
    board = bored.niceBoard()
    message = 'cont'
    bored.next()

    emit("new state", (board, message))



@socketio.on("input move")
def input(move):

    selection = move["move"]
    token = np.unravel_index(int(selection),(3,3))

    if bored.addToken(token[0],token[1]) == "bad": # add token and check if it is a valid input
        return emit("invalid")

    board = bored.niceBoard()
    end, message = bored.getMessage()

    if end == True:
        return emit("new state", (board, message))

    bored.next()
    bored.agentMove()
    board = bored.niceBoard()
    end, message = bored.getMessage()

    if end == True:
        return emit("new state", (board, message))

    bored.next()

    emit("new state", (board, message))


if __name__ == '__main__':
    socketio.run(app)
