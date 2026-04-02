# author: Sam
# description: Packers Dashboard Flask App

from flask import Flask, render_template, redirect, url_for, flash, request
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# ===============================
# HOME DASHBOARD (SHOW ALL TABLES)
# ===============================
@app.route("/")
def home():
    players = get_all_players()
    stats = get_player_stats()
    games = get_games()

    return render_template(
        "index.html",
        players=players,
        stats=stats,
        games=games
    )


# ===============================
# ROSTER PAGE
# ===============================
@app.route("/roster")
def roster():
    players = get_all_players()
    return render_template("roster.html", players=players)


# ===============================
# PLAYER STATS PAGE
# ===============================
@app.route("/playerstats")
def playerstats():
    stats = get_player_stats()
    return render_template("playerstats.html", stats=stats)


# ===============================
# GAMES PAGE
# ===============================
@app.route("/games")
def games():
    games = get_games()
    return render_template("games.html", games=games)


# ===============================
# ADD PLAYER (UPDATED FOR YOUR SCHEMA)
# ===============================
@app.route("/add-player", methods=["POST"])
def add_player():
    name = request.form["name"]
    position = request.form["position"]
    jersey = request.form["jersey"]
    height = request.form["height"]
    weight = request.form["weight"]

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO players (name, position, jersey, height, weight)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (name, position, jersey, height, weight)
    )

    conn.commit()
    conn.close()

    flash("Player added successfully!")
    return redirect(url_for("roster"))


# ===============================
# DELETE PLAYER
# ===============================
@app.route("/delete-player/<int:id>")
def delete_player(id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM players WHERE player_id = %s", (id,))

    conn.commit()
    conn.close()

    flash("Player deleted.")
    return redirect(url_for("roster"))


# ===============================
# UPDATE PLAYER JERSEY
# ===============================
@app.route("/update-player/<int:id>", methods=["POST"])
def update_player(id):
    jersey = request.form["jersey"]

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE players SET jersey = %s WHERE player_id = %s",
        (jersey, id)
    )

    conn.commit()
    conn.close()

    flash("Player updated successfully!")
    return redirect(url_for("roster"))


# ===============================
# RUN APP
# ===============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)