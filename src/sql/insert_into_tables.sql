-- dim_team
INSERT INTO dim_team(posteam)
SELECT DISTINCT posteam
FROM nfl_pbp_raw
ON CONFLICT (posteam) DO NOTHING;

-- dim_play_types
INSERT INTO dim_play_types(play_type)
SELECT DISTINCT playtype
FROM nfl_pbp_raw
ON CONFLICT (play_type) DO NOTHING;

-- dim_game
INSERT INTO dim_game(game_id, game_date, home_team, away_team, season)
SELECT DISTINCT gameid, date, hometeam, awayteam, season
FROM nfl_pbp_raw
ON CONFLICT (game_id) DO NOTHING;

-- dim_plays
INSERT INTO dim_plays(
    game_id,
    posteam,
    defensive_team,
    play_type,
    yards_gained,
    down,
    is_positive_run,
    is_positive_pass
)
SELECT
    gameid,
    posteam,
    defensiveteam,
    playtype,
    yards_gained,
    down,
    CASE WHEN playtype = 'Run' AND yards_gained > 0 THEN 1 ELSE 0 END,
    CASE WHEN playtype = 'Pass' AND yards_gained > 0 THEN 1 ELSE 0 END
FROM nfl_pbp_raw;

-- dim_num_play_types
INSERT INTO dim_num_play_types(posteam, total_run, total_pass)
SELECT 
    posteam,
    SUM(CASE WHEN play_type = 'Run' THEN 1 ELSE 0 END),
    SUM(CASE WHEN play_type = 'Pass' THEN 1 ELSE 0 END)
FROM dim_plays
GROUP BY posteam
ON CONFLICT (posteam) DO UPDATE
SET total_run = EXCLUDED.total_run,
    total_pass = EXCLUDED.total_pass;

-- total_team_facts
INSERT INTO total_team_facts(
    posteam,
    total_plays,
    run_plays,
    pass_plays,
    pos_run,
    pos_pass
)
SELECT 
    t.posteam,
    COUNT(p.play_id) AS total_plays,
    MAX(n.total_run) AS run_plays,
    MAX(n.total_pass) AS pass_plays,
    ROUND(SUM(p.is_positive_run)::numeric / COUNT(p.play_id), 4) * 100 AS pos_run,
    ROUND(SUM(p.is_positive_pass)::numeric / COUNT(p.play_id), 4) * 100 AS pos_pass
FROM dim_team AS t
JOIN dim_plays AS p
    ON t.posteam = p.posteam
JOIN dim_num_play_types AS n
    ON t.posteam = n.posteam
GROUP BY t.posteam
ON CONFLICT (posteam) DO UPDATE
SET total_plays = EXCLUDED.total_plays,
    run_plays = EXCLUDED.run_plays,
    pass_plays = EXCLUDED.pass_plays,
    pos_run = EXCLUDED.pos_run,
    pos_pass = EXCLUDED.pos_pass;