CREATE TABLE IF NOT EXISTS dim_team(
    posteam TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS dim_play_types(
    play_type TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS dim_game(
    game_id INTEGER PRIMARY KEY,
    game_date DATE,
    home_team TEXT,
    away_team TEXT,
    season INTEGER
);

CREATE TABLE IF NOT EXISTS dim_plays(
    play_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT,
    posteam TEXT,
    defensive_team TEXT,
    play_type TEXT,
    yards_gained INTEGER,
    down INTEGER,
    is_positive_run INTEGER,
    is_positive_pass INTEGER,
    FOREIGN KEY(game_id) REFERENCES dim_game(game_id),
    FOREIGN KEY(posteam) REFERENCES dim_team(posteam),
    FOREIGN KEY(defensive_team) REFERENCES dim_team(posteam),
    FOREIGN KEY(play_type) REFERENCES dim_play_types(play_type)
);

CREATE TABLE IF NOT EXISTS dim_num_play_types(
    posteam TEXT PRIMARY KEY,
    total_run INTEGER,
    total_pass INTEGER,
    FOREIGN KEY (posteam) REFERENCES dim_team(posteam)
);

CREATE TABLE IF NOT EXISTS total_team_facts(
    posteam TEXT PRIMARY KEY,
    total_plays INTEGER,
    run_plays INTEGER,
    pass_plays INTEGER,
    pos_run FLOAT,
    pos_pass FLOAT,
    FOREIGN KEY(posteam) REFERENCES dim_team(posteam)
);