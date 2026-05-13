from flask import Flask, render_template
from flask import request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is running!"

@app.route("/local")
def local():
    return render_template("local.html")

@app.route("/online")
def online():
    return "<h2>Online mode coming soon</h2>"

def empty_cells(board):
    return [i for i,v in enumerate(board) if v==""]

def random_move(board):
    moves = empty_cells(board)
    return random.choice(moves) if moves else None

def winner(board):
    lines=[
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in lines:
        if board[a] and board[a]==board[b]==board[c]:
            return board[a]
    return None

def winning_move(board,player):
    for i in empty_cells(board):
        board[i]=player
        if winner(board)==player:
            board[i]=""
            return i
        board[i]=""
    return None

@app.route("/api/ai-move", methods=["POST"])
def ai_move():
    data=request.json
    board=data["board"]
    diff=data["difficulty"]

    if diff=="easy":
        move=random_move(board)

    elif diff=="medium":
        move=winning_move(board,"O")
        if move is None:
            move=winning_move(board,"X")
        if move is None:
            move=random_move(board)

    else:
        move=random_move(board)

    return jsonify({"move":move})

if __name__ == "__main__":
    app.run(debug=True)
