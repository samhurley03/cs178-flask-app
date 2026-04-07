# dbCode.py
# Author: Sam
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        database=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )

def get_all_players():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players;")
    result = cursor.fetchall()
    conn.close()
    return result

def get_player_stats():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT players.name, players.position, stats.passing_yards,
               stats.rushing_yards, stats.touchdowns
        FROM players
        JOIN stats ON players.player_id = stats.player_id;
    """)

    result = cursor.fetchall()
    conn.close()
    return result

def get_games():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *,
        CASE 
            WHEN points_for > points_against THEN 'Win'
            ELSE 'Loss'
        END as result
        FROM games
        ORDER BY game_date
    """)

    games = cursor.fetchall()
    conn.close()
    return games

def get_dashboard_summary():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_players FROM players")
    total_players = cursor.fetchone()["total_players"]

    cursor.execute("SELECT COUNT(*) as total_games FROM games")
    total_games = cursor.fetchone()["total_games"]

    cursor.execute("SELECT SUM(touchdowns) as total_tds FROM stats")
    total_tds = cursor.fetchone()["total_tds"]

    cursor.execute("""
        SELECT 
        SUM(CASE WHEN points_for > points_against THEN 1 ELSE 0 END) as wins,
        COUNT(*) as total
        FROM games
    """)
    record = cursor.fetchone()

    conn.close()

    win_pct = round((record["wins"] / record["total"]) * 100, 1) if record["total"] > 0 else 0

    return total_players, total_games, total_tds, win_pct
