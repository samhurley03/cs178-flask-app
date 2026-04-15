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

    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        # must match full row structure (8 columns)
        if len(cols) < 8:
            continue

        try:
            name = cols[0].get_text(strip=True)
            jersey = cols[1].get_text(strip=True)
            position = cols[2].get_text(strip=True)
            height = cols[3].get_text(strip=True)
            weight = cols[4].get_text(strip=True)

            # skip headers / bad rows
            if name.lower() in ["player", "name"]:
                continue

            if not name or not jersey:
                continue

            players.append((name, position, jersey, height, weight))

        except Exception:
            continue

    return players


# =========================
# UPSERT INTO DATABASE
# =========================
def upsert_players(players):
    conn = get_conn()
    cursor = conn.cursor()

    seen = set()
    clean = []

    for p in players:
        if p[0] not in seen:
            clean.append(p)
            seen.add(p[0])

    for name, position, jersey, height, weight in clean:
        cursor.execute("""
            INSERT INTO players (name, position, jersey, height, weight)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                position = VALUES(position),
                jersey = VALUES(jersey),
                height = VALUES(height),
                weight = VALUES(weight)
        """, (name, position, jersey, height, weight))

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