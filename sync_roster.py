import requests
from bs4 import BeautifulSoup
import pymysql

URL = "https://www.packers.com/team/players-roster/"

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="packers_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def scrape_roster():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    players = []

    # NOTE: website structure may change
    rows = soup.select("tr.ClubRoster_tr__*")  # sometimes dynamic class names

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        name = cols[0].get_text(strip=True)
        position = cols[1].get_text(strip=True)
        jersey = cols[2].get_text(strip=True)

        players.append((name, position, jersey))

    return players


def upsert_players(players):
    conn = get_conn()
    cursor = conn.cursor()

    for name, position, jersey in players:
        cursor.execute("""
            INSERT INTO players (name, position, jersey)
            VALUES (%s, %s, %s)
        """, (name, position, jersey))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    players = scrape_roster()
    upsert_players(players)
    print(f"Inserted {len(players)} players")