# dbCode.py
# Author: Your Name
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
    cursor.execute("SELECT * FROM games;")
    result = cursor.fetchall()
    conn.close()
    return result
