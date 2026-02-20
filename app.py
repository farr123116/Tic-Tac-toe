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


@app.route("/api/ai-move", methods=["POST"])
def ai_move():
    data=request.json
    board=data["board"]
    difficulty=data["difficulty"]

    move = random_move(board)

    return jsonify({"move":move})

if __name__ == "__main__":
    app.run(debug=True)
