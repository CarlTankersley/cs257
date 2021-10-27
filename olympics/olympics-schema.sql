CREATE TABLE athletes (
    id INT,
    name TEXT,
    sex TEXT,
    height INT,
    weight NUMERIC
);

CREATE TABLE events (
    id INT,
    sport TEXT,
    event TEXT
);

CREATE TABLE games (
    id INT,
    year INT,
    season TEXT,
    city TEXT
);

CREATE TABLE medals (
    id INT,
    medal TEXT
);

CREATE TABLE teams (
    id INT,
    noc TEXT,
    country TEXT
);

CREATE TABLE links (
    athlete_id INT,
    event_id INT,
    games_id INT,
    medal_id INT,
    team_id INT
);