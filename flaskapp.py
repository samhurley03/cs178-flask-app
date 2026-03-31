# author: Sam
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, redirect, url_for, flash, jsonify
import requests
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

TEAM_ID = 9

ROSTER = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/roster"
SCHEDULE = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/schedule"
SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
STATS = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/statistics"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/roster")
def roster():
    data = requests.get(ROSTER).json()
    players = []

    for g in data["athletes"]:
        for p in g["items"]:
            players.append({
                "name": p["fullName"],
                "position": g["position"],
                "jersey": p.get("jersey","")
            })

    return jsonify(players)


@app.route("/api/schedule")
def schedule():

    data = requests.get(SCHEDULE).json()
    games = []

    for g in data["events"]:

        comp = g["competitions"][0]

        games.append({
            "week": g["week"]["number"],
            "home": comp["competitors"][0]["team"]["displayName"],
            "away": comp["competitors"][1]["team"]["displayName"],
            "status": g["status"]["type"]["shortDetail"]
        })

    return jsonify(games)


@app.route("/api/scores")
def scores():

    data = requests.get(SCOREBOARD).json()
    games = []

    for g in data["events"]:

        comp = g["competitions"][0]

        games.append({
            "home": comp["competitors"][0]["team"]["displayName"],
            "away": comp["competitors"][1]["team"]["displayName"],
            "homeScore": comp["competitors"][0]["score"],
            "awayScore": comp["competitors"][1]["score"],
            "status": g["status"]["type"]["shortDetail"]
        })

    return jsonify(games)

@app.route("/api/teamstats")
def teamstats():

    TEAM_STATS_API = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/9/statistics"

    r = requests.get(TEAM_STATS_API)
    data = r.json()

    stats = []

    try:
        categories = data["results"]["stats"]["categories"]

        for category in categories:
            for stat in category["stats"]:
                stats.append({
                    "name": stat["displayName"],
                    "value": stat["displayValue"]
                })

    except:
        stats.append({
            "name": "Stats unavailable",
            "value": "-"
        })

    return jsonify(stats)


# ADD SECTION 4 HERE
@app.route("/api/leaders")
def leaders():

    url="https://site.api.espn.com/apis/site/v2/sports/football/nfl/statistics"
    data=requests.get(url).json()

    leaders=[]

    for cat in data["leaders"]:
        leaders.append({
            "category":cat["displayName"],
            "leader":cat["leaders"][0]["athlete"]["displayName"],
            "value":cat["leaders"][0]["displayValue"]
        })

    return jsonify(leaders)

@app.route("/api/schedule_last_year")
def schedule_last_year():

    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/9/schedule?season=2024"

    data = requests.get(url).json()

    games = []

    for g in data["events"]:

        comp = g["competitions"][0]

        games.append({
            "week": g["week"]["number"],
            "home": comp["competitors"][0]["team"]["displayName"],
            "away": comp["competitors"][1]["team"]["displayName"],
            "status": g["status"]["type"]["shortDetail"]
        })

    return jsonify(games)

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
