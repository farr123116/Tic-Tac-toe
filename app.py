from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)
