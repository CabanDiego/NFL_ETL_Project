'''Module to read and clean CSV file'''
import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

def read_and_load(source: Path,):
    '''Read and clean csv into chunks'''

    #Verify data file is in folder
    if not source.exists():
        logger.error("Data File Was not Found")
        raise FileNotFoundError(f"The source file {source} does not exist.")

    #Columns for renaming
    rename_cols = {
        "Yards.Gained" : "Yards_Gained",
        "Challenge.Replay" : "Challenge_Replay",
        "Accepted.Penalty" : "Accepted_Penalty",
        "Penalty.Yards" : "Penalty_Yards"
    }

    chunksize = 5000
    logger.info(f"Chunking Data in chunks of {chunksize}")
    
    #Unwanted Columns from original
    unneeded_cols = ['TimeUnder', 'TimeSecs', 'PlayTimeDiff', 'yrdline100',
                     'sp', 'ExPointResult', 'TwoPointConv', 'DefTwoPoint',
                     'Safety', 'Onsidekick', 'PuntResult', 'PassLocation',
                     'RunGap', 'ReturnResult', 'Returner', 'BlockingPlayer',
                     'Tackler1', 'Tackler2', 'FieldGoalResult', 'FieldGoalDistance',
                     'Fumble', 'RecFumbTeam', 'RecFumbPlayer', 'PenaltyType',
                     'PenalizedPlayer', 'PosTeamScore', 'DefTeamScore', 'ScoreDiff',
                     'AbsScoreDiff', 'Timeout_Indicator', 'Timeout_Team', 'posteam_timeouts_pre',
                     'HomeTimeouts_Remaining_Pre', 'AwayTimeouts_Remaining_Pre', 
                     'HomeTimeouts_Remaining_Post','AwayTimeouts_Remaining_Post', 'No_Score_Prob', 
                     'Opp_Field_Goal_Prob', 'Opp_Safety_Prob','Opp_Touchdown_Prob', 
                     'Field_Goal_Prob', 'Safety_Prob', 'Touchdown_Prob', 'ExPoint_Prob', 
                     'TwoPoint_Prob', 'ExpPts,EPA', 'airEPA', 'yacEPA', 'Home_WP_pre',
                     'Away_WP_pre', 'Home_WP_post','Away_WP_post', 'Win_Prob', 
                     'WPA', 'airWPA', 'yacWPA']

    #Looping through each chunk to send to db
    for chunk in pd.read_csv(source, chunksize=chunksize):
        
        #Drop unwanted columns
        cols_to_drop = [c for c in unneeded_cols if c in chunk.columns]
        chunk = chunk.drop(columns=cols_to_drop)

        #Rename columns
        rename_exists = {k: v for k, v in rename_cols.items() if k in chunk.columns}
        chunk = chunk.rename(columns=rename_exists)
        
        #Strip whitespace from columns
        for col in chunk.select_dtypes(include="object").columns:
            chunk[col] = chunk[col].str.strip()

        #Only drop rows where posteam is empty or missing
        if "posteam" in chunk.columns:
            chunk = chunk[chunk["posteam"].notna() & (chunk["posteam"] != "")]

        #Capitalize the PlayType column to make it easier to query
        if "PlayType" in chunk.columns:
            chunk["PlayType"] = chunk["PlayType"].str.title()
        
        #Yield the cleaned chunk to be loaded into db
        yield chunk
