# sync_roster.py
# Author: Sam
# Purpose: Sync Packers roster into MySQL database

import requests
from bs4 import BeautifulSoup
import pymysql
import creds


URL = "https://www.packers.com/team/players-roster/"


# =========================
# DATABASE CONNECTION
# =========================
def get_conn():
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        database=creds.db,
        cursorclass=pymysql.cursors.DictCursor
    )


# =========================
# SCRAPE ROSTER
# =========================
def scrape_roster():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    players = []

    # safer generic approach (since site is JS-heavy / unstable)
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        # skip invalid rows
        if len(cols) < 3:
            continue

        try:
            name = cols[0].get_text(strip=True)
            position = cols[1].get_text(strip=True)
            jersey = cols[2].get_text(strip=True)

            # basic cleanup
            if name and position:
                players.append((name, position, jersey))

        except Exception:
            continue

    return players


# =========================
# UPSERT INTO DATABASE
# =========================
def upsert_players(players):
    conn = get_conn()
    cursor = conn.cursor()

    # optional: reduce duplicates from scraping
    seen = set()
    clean_players = []

    for p in players:
        if p[0] not in seen:
            clean_players.append(p)
            seen.add(p[0])

    for name, position, jersey in clean_players:
        cursor.execute("""
            INSERT INTO players (name, position, jersey)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                position = VALUES(position),
                jersey = VALUES(jersey)
        """, (name, position, jersey))

    conn.commit()
    cursor.close()
    conn.close()


# =========================
# MAIN RUN
# =========================
if __name__ == "__main__":
    print("Scraping roster...")
    players = scrape_roster()

    print(f"Found {len(players)} players")

    print("Updating database...")
    upsert_players(players)

    print("Done ✔")