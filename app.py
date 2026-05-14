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


def minimax(board, maximizing, depth=0, alpha=-10, beta=10):
    w = winner(board)
    if w == "O": return 10 - depth
    if w == "X": return depth - 10
    if is_full(board): return 0

    if maximizing:
        best = -10
        for i in empty_cells(board):
            board[i] = "O"
            score = minimax(board, False, depth + 1, alpha, beta)
            board[i] = ""
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = 10
        for i in empty_cells(board):
            board[i] = "X"
            score = minimax(board, True, depth + 1, alpha, beta)
            board[i] = ""
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def best_move(board):
    best_score = -99
    move = None
    if not empty_cells(board):
        return None
    if len(empty_cells(board)) == 9 and board[4] == "":
        return 4
    for i in empty_cells(board):
        board[i] = "O"
        score = minimax(board, False)
        board[i] = ""
        if score > best_score:
            best_score = score
            move = i
    return move


@app.route("/api/ai-move", methods=["POST"])
def ai_move():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    board = data.get("board")
    diff = data.get("difficulty", "medium")

    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Invalid board"}), 400
    if any(v not in ("", "X", "O") for v in board):
        return jsonify({"error": "Invalid cell values"}), 400
    if winner(board) or is_full(board):
        return jsonify({"error": "Game already over"}), 400

    if diff == "easy":
        move = random_move(board)
    elif diff == "medium":
        move = (winning_move(board, "O") or winning_move(board, "X") or random_move(board))
    elif diff == "hard":
        move = (random_move(board) if random.random() < 0.25
                else winning_move(board, "O") or winning_move(board, "X") or best_move(board))
    else:
        move = best_move(board)

    board[move] = "O"
    w = winner(board)
    line = winning_line(board) if w else None
    draw = is_full(board) and not w
    board[move] = ""

    return jsonify({"move": move, "winner": w, "winning_line": line, "draw": draw})


@app.route("/api/check", methods=["POST"])
def check_board():
    data = request.get_json(silent=True) or {}
    board = data.get("board", [])
    if len(board) != 9:
        return jsonify({"error": "Bad board"}), 400

    w = winner(board)
    line = winning_line(board) if w else None
    draw = is_full(board) and not w

    return jsonify({"winner": w, "winning_line": line, "draw": draw})


if __name__ == "__main__":
    app.run(debug=True)
