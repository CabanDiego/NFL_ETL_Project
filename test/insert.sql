INSERT OR REPLACE INTO dim_team(posteam)
    SELECT DISTINCT posteam FROM plays;

INSERT OR REPLACE INTO dim_play_types(play_type)
    SELECT DISTINCT PlayType FROM plays;

INSERT OR REPLACE INTO dim_game(game_id, game_date, home_team, away_team, season)
    SELECT DISTINCT GameID, Date, HomeTeam, AwayTeam, Season FROM plays;

INSERT OR REPLACE INTO dim_plays(
    game_id,
    posteam,
    defensive_team,
    play_type,
    yards_gained,
    down,
    is_positive_run,
    is_positive_pass) 
        SELECT
        GameID,
        posteam,
        DefensiveTeam,
        PlayType,
        Yards_Gained,
        down,
        CASE WHEN PlayType = 'Run' AND Yards_Gained > 0 THEN 1 ELSE 0 END,
        CASE WHEN PlayType = 'Pass' AND Yards_Gained > 0 THEN 1 ELSE 0 END
FROM plays;


INSERT OR REPLACE INTO dim_num_play_types(posteam, total_run, total_pass)
    SELECT 
    posteam,
    SUM(CASE WHEN play_type = 'Run' THEN 1 ELSE 0 END),
    SUM(CASE WHEN play_type = 'Pass' THEN 1 ELSE 0 END)
FROM dim_plays
GROUP BY posteam;

INSERT OR REPLACE INTO total_team_facts(
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
    n.total_run,
    n.total_pass,
    ROUND(SUM(p.is_positive_run) * 1.0 / COUNT(p.play_id), 4) * 100 AS pos_run,
    ROUND(SUM(p.is_positive_pass) * 1.0 / COUNT(p.play_id), 4) * 100 AS pos_pass
    FROM dim_team AS t
    JOIN dim_plays AS p
        ON t.posteam = p.posteam
    JOIN dim_num_play_types AS n
        ON t.posteam = n.posteam
    GROUP BY t.posteam;