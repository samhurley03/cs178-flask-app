# Packers_db

**CS178: Cloud and Database Systems — Project #1**
**Author:** Sam
**GitHub:** samhurley03

---

## Overview

<!-- My project is a Flask web application connected to an Amazon RDS MySQL database that manages Green Bay Packers player data and statistics. It allows users to create, view, update, and delete player records and associated stats through a web interface. The application is designed for coaches, analysts, or fans who want an organized way to manage and track player performance data. It solves the problem of manually managing roster and stats information by storing everything in a structured, centralized database accessible through a user-friendly website. -->

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database used to store structured data such as players, games, and player statistics. This includes player names, positions, teams, game results, and statistical performance data that require relationships between tables (e.g., players linked to games and stats).
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — non-relational database used to store flexible or supplemental data such as user interactions, logs, or additional metadata that does not require strict relational structure. This allows for scalable, fast access to key-value or document-based data without enforcing table relationships.
---

## Project Structure

```
CS_178_New/
└── cs178-flask-app/
    ├── .github/
    │   └── workflows/
    │       └── deploy.yml              # GitHub Actions deployment workflow
    ├── static/                         # CSS, images, JS files
    ├── templates/
    │   ├── add_user.html               # Form to add a new user/player
    │   ├── delete_player.html          # Page to delete a player
    │   ├── display_users.html          # Displays users from database
    │   ├── edit_player.html            # Edit/update player information
    │   ├── games.html                  # Displays games data
    │   ├── home.html                   # Home page
    │   ├── index.html                  # Main landing page
    │   ├── layout.html                 # Base template layout
    │   ├── players.html                # Displays player list
    │   └── playerstats.html            # Displays player statistics
    ├── .gitignore                      # Excludes creds.py and sensitive files
    ├── creds.py                        # Database credentials (NOT pushed to GitHub)
    ├── dbCode.py                       # MySQL database helper functions
    ├── dynamoCode.py                   # DynamoDB helper functions
    ├── flaskapp.py                     # Main Flask application (routes + logic)
    ├── packers_db.sql                  # Database schema and seed data
    └── README.md                       # Project documentation
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/samhurley03/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `ec2-54-166-250-119.compute-1.amazonaws.com:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
ec2-54-166-250-119.compute-1.amazonaws.com:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `[players]` — stores [player information such as player_id, name, position, jersey number, and team]; primary key is `[player_id]`
- `[stats]` — stores [stores individual player statistics such as touchdowns and passing yards]; foreign key player_id links to `[players]`
- `[games]` — stores [player information such as player_id, name, position, jersey number, and team]; primary key is `[player_id]`

The JOIN query used in this project: <!-- The JOIN query combines the players and stats tables so the app can display player names alongside their statistical performance. -->

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `[packers-pageviews]`
- **Partition key:** `[page]`
- **Used for:** `[Displays how many time users visit the Games webpage]`

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/add_player` | [Inserts a new player record into the players table in RDS.] |
| Read      | `/roster` | [Retrieves and displays all players from the players table.] |
| Update    | `/edit_player` | [Updates an existing player’s information in the players table.] |
| Delete    | `/delete_player` | [Deletes a player record from the players table (after handling related stats due to foreign key constraints).] |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions?
Understanding how to make the webpage run continually was my biggest challenge. It was the most difficult thing to implement but understanding the behind the scenes was difficult. -->

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here.

I used AI for only the README file. It helped to describe my filepaths and tables concisely.   -->
