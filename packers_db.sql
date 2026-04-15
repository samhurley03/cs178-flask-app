CREATE DATABASE IF NOT EXISTS packers_db;
USE packers_db;

CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50),
    jersey INT,
    height VARCHAR(10),
    weight INT
);

CREATE TABLE games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    opponent VARCHAR(100),
    game_date DATE,
    home_away VARCHAR(10),
    points_for INT,
    points_against INT

   
);

CREATE TABLE stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    season INT,
    passing_yards INT,
    rushing_yards INT,
    touchdowns INT,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);



INSERT INTO games (opponent, game_date, home_away, points_for, points_against)
VALUES
('Bears', '2024-09-10', 'Home', 27, 17),
('Vikings', '2024-09-17', 'Away', 21, 24);

INSERT INTO stats (player_id, season, passing_yards, rushing_yards, touchdowns)
VALUES
(1, 2024, 4100, 200, 32),
(2, 2024, 200, 1100, 10),
(3, 2024, 0, 0, 7);

ALTER TABLE players ADD UNIQUE (name);