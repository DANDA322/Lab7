CREATE SCHEMA IF NOT EXISTS UEFA;

CREATE TABLE IF NOT EXISTS UEFA.teams
(
    team_name    text NOT NULL PRIMARY KEY,
    country      text NOT NULL,
    home_stadium text NOT NULL
);

CREATE TABLE IF NOT EXISTS UEFA.stadiums
(
    name     text    NOT NULL PRIMARY KEY,
    city     text    NOT NULl,
    country  text    NOT NULL,
    capacity integer NOT NULL
);

CREATE TABLE IF NOT EXISTS UEFA.players
(
    player_id     text    NOT NULL PRIMARY KEY,
    first_name    text    NOT NULl DEFAULT '',
    last_name     text    NOT NULL DEFAULT '',
    nationality   text    NOT NULL DEFAULT '',
    dob           date    NULL,
    team          text    NOT NULL DEFAULT '',
    jersey_number text    NOT NULL DEFAULT '',
    position      text    NOT NULL DEFAULT '',
    height        integer NOT NULL DEFAULT -1,
    weight        integer NOT NULL DEFAULT -1,
    foot          text    NOT NULL DEFAULT ''
);

DROP TABLE UEFA.players;

CREATE TABLE IF NOT EXISTS UEFA.managers
(
    first_name  text      NOT NULl DEFAULT '',
    last_name   text      NOT NULL DEFAULT '',
    nationality text      NOT NULL DEFAULT '',
    dob         date NOT NULL,
    team        text      NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS UEFA.matches
(
    match_id          text    NOT NULl DEFAULT '' PRIMARY KEY,
    season            text    NOT NULl DEFAULT '',
    date_time         timestamp        DEFAULT NULL,
    home_team         text    NOT NULl DEFAULT '',
    away_team         text    NOT NULl DEFAULT '',
    stadium           text    NOT NULl DEFAULT '',
    home_team_score   integer NOT NULL DEFAULT 0,
    away_team_score   integer NOT NULL DEFAULT 0,
    penalty_shoot_out integer NOT NULL DEFAULT 0,
    attendance        integer NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS UEFA.goals
(
    goal_id   text    NOT NULl DEFAULT '' PRIMARY KEY,
    match_id  text    NOT NULl DEFAULT '',
    player_id text    NOT NULl DEFAULT '',
    duration  integer NOT NULl DEFAULT 0,
    assist    text    NOT NULl DEFAULT '',
    goal_desc text    NOT NULL DEFAULT ''
);