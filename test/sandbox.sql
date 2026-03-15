.headers on
--Creating play types dim table
CREATE TABLE IF NOT EXISTS dim_play_types(
    posteam TEXT PRIMARY KEY,
    total_plays INTEGER,
    run_plays INTEGER,
    pass_plays INTEGER
);

--Populating play types dim table
INSERT OR REPLACE INTO dim_play_types (posteam, total_plays, run_plays, pass_plays)
SELECT 
    posteam,
    COUNT(*) AS total_plays,
    --Using SUM  of cases to seperate play types, it adds 1 if the column has that specific play type                               
    SUM(CASE WHEN PlayType = 'Run' THEN 1 ELSE 0 END) AS run_plays,
    SUM(CASE WHEN PlayType = 'Pass' THEN 1 ELSE 0 END) AS pass_plays
FROM plays
--Grouping each stat by team
GROUP BY posteam;                                 


SELECT * FROM dim_play_types;