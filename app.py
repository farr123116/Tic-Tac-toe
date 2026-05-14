from flask import Flask, render_template
from flask import request, jsonify
import random

app = Flask(__name__)
app.secret_key = "tictactoe_secret_key_2024"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/local")
def local():
    return render_template("local.html")

@app.route("/online")
def online():
    return render_template("online.html")

def empty_cells(board):
    return [i for i,v in enumerate(board) if v==""]

LINES = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def winner(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def winning_line(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return [a, b, c]
    return None

def is_full(board):
    return "" not in board

def random_move(board):
    moves = empty_cells(board)
    return random.choice(moves) if moves else None

def winning_move(board,player):
    for i in empty_cells(board):
        board[i]=player
        if winner(board)==player:
            board[i]=""
            return i
        board[i]=""
    return None

def minimax(board, maximizing):
    win=winner(board)
    if win=="O": return 1
    if win=="X": return -1
    if "" not in board: return 0

    if maximizing:
        best=-9
        for i in empty_cells(board):
            board[i]="O"
            best=max(best,minimax(board,False))
            board[i]=""
        return best
    else:
        best=9
        for i in empty_cells(board):
            board[i]="X"
            best=min(best,minimax(board,True))
            board[i]=""
        return best


def best_move(board):
    best=-9
    move=None
    for i in empty_cells(board):
        board[i]="O"
        score=minimax(board,False)
        board[i]=""
        if score>best:
            best=score
            move=i
    return move

@app.route("/api/ai-move", methods=["POST"])
def ai_move():
    data=request.json
    board=data["board"]
    diff=data["difficulty"]

    if diff=="easy":
        move=random_move(board)

    elif diff=="medium":
        move=winning_move(board,"O") or winning_move(board,"X") or random_move(board)

    elif diff=="hard":
        if random.random()<0.3:
            move=random_move(board)
        else:
            move=best_move(board)

    else:  # unbeatable
        move=best_move(board)

    return jsonify({"move":move})

if __name__ == "__main__":
    app.run(debug=True)
