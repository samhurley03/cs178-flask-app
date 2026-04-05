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
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html        # Landing page
│   ├── [other].html     # Add descriptions for your other templates
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
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

- `[TableName]` — stores [description]; primary key is `[key]`
- `[TableName]` — stores [description]; foreign key links to `[other table]`

The JOIN query used in this project: <!-- describe it in plain English -->

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `[your-table-name]`
- **Partition key:** `[key-name]`
- **Used for:** [description]

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/[route]` | [what it does] |
| Read      | `/[route]` | [what it does] |
| Update    | `/[route]` | [what it does] |
| Delete    | `/[route]` | [what it does] |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->

---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
