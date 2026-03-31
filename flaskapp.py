# author: Sam
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, redirect, url_for, flash, jsonify
import creds
import requests
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone




@app.route("/")
def home():
    return render_template("index.html")


@app.route("/roster")
def roster():
    players = get_all_players()
    return render_template("roster.html", players=players)


@app.route("/playerstats")
def playerstats():
    stats = get_player_stats()
    return render_template("playerstats.html", stats=stats)


@app.route("/games")
def games():
    games = get_games()
    return render_template("games.html", games=games)

@app.route("/add-player", methods=["POST"])
def add_player():
    name = requests.form["name"]
    position = requests.form["position"]
    jersey = requests.form["jersey"]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO players (name, position, jersey) VALUES (%s,%s,%s)",
        (name, position, jersey)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("roster"))

@app.route("/delete-player/<int:id>")
def delete_player(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE player_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("roster"))

@app.route("/update-player/<int:id>", methods=["POST"])
def update_player(id):
    jersey = requests.form["jersey"]

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE players SET jersey=%s WHERE player_id=%s",
        (jersey, id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("roster"))





# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
