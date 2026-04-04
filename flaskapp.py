# author: Sam
# description: Packers Dashboard Flask App

from flask import Flask, render_template, redirect, url_for, flash, request
from dynamoCode import log_page_view
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# ===============================
# HOME DASHBOARD (SHOW ALL TABLES)
# ===============================
from dynamoCode import get_page_view_count

@app.route("/")
def home():
    players = get_all_players()
    stats = get_player_stats()
    games = get_games()

    games_views = get_page_view_count("games")

    return render_template(
        "index.html",
        players=players,
        stats=stats,
        games=games,
        games_views=games_views
    )


# ===============================
# ROSTER PAGE
# ===============================
@app.route("/roster")
def roster():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    conn.close()
    return render_template("players.html", players=players)




# ===============================
# GAMES PAGE
# ===============================
@app.route("/games")
def games():
    log_page_view("games", request.remote_addr)

    games = get_games()
    return render_template("games.html", games=games)


# ===============================
# ADD PLAYER (UPDATED FOR YOUR SCHEMA)
# ===============================
@app.route("/add-player", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
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

    # GET request just shows the form
    return render_template("add_user.html")

@app.route("/edit-player/<int:player_id>", methods=["GET", "POST"])
def edit_player(player_id):
    conn = get_conn()
    cursor = conn.cursor()
    
    # Fetch existing player
    cursor.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
    player = cursor.fetchone()
    
    if request.method == "POST":
        name = request.form["name"]
        position = request.form["position"]
        jersey = request.form["jersey"]
        height = request.form["height"]
        weight = request.form["weight"]
        
        cursor.execute(
            """
            UPDATE players
            SET name=%s, position=%s, jersey=%s, height=%s, weight=%s
            WHERE player_id=%s
            """,
            (name, position, jersey, height, weight, player_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("roster"))
    
    conn.close()
    return render_template("edit_player.html", player=player)


# ===============================
# DELETE PLAYER
# ===============================
@app.route("/delete-player/<int:player_id>", methods=["GET", "POST"])
def delete_player(player_id):
    conn = get_conn()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
        player = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template("delete_player.html", player=player)

    # POST: delete stats first, then player
    try:
        cursor.execute("DELETE FROM stats WHERE player_id = %s", (player_id,))
        cursor.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for("roster"))

@app.route("/player-stats")
def playerstats():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.player_id, p.name, p.position, s.games_played, s.points, s.rebounds, s.assists
        FROM players p
        LEFT JOIN stats s ON p.player_id = s.player_id
    """)
    stats = cursor.fetchall()  # returns a list of dicts
    cursor.close()
    conn.close()
    return render_template("playerstats.html", stats=stats)



# ===============================
# RUN APP
# ===============================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)