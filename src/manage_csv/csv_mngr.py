'''Module to read and clean CSV file'''
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def manage_file(source: Path, output: Path):
    '''Read, Clean, and output new csv'''
    
    #Verify data file is in folder
    if not source.exists():
        raise FileNotFoundError(f"The source file {source} does not exist.")
    
    #Columns for renaming
    rename_cols = {
        "Yards.Gained" : "Yards_Gained",
        "Challenge.Replay" : "Challenge_Replay",
        "Accepted.Penalty" : "Accepted_Penalty",
        "Penalty.Yards" : "Penalty_Yards"
    }

    chunksize = 500
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
                     'HomeTimeouts_Remaining_Pre', 'AwayTimeouts_Remaining_Pre', 'HomeTimeouts_Remaining_Post',
                     'AwayTimeouts_Remaining_Post', 'No_Score_Prob', 'Opp_Field_Goal_Prob', 'Opp_Safety_Prob',
                     'Opp_Touchdown_Prob', 'Field_Goal_Prob', 'Safety_Prob', 'Touchdown_Prob', 'ExPoint_Prob',
                     'TwoPoint_Prob', 'ExpPts,EPA', 'airEPA', 'yacEPA', 'Home_WP_pre',' Away_WP_pre', 'Home_WP_post',
                     'Away_WP_post', 'Win_Prob', 'WPA', 'airWPA', 'yacWPA']
    
    #Looping through each chunk using enumerate to see which chunk it is for headers
    for i, chunk in enumerate(pd.read_csv(source, chunksize=chunksize)):
        #Dropping columns
        #Looping through in case columns are missing for a row
        cols_to_drop = [c for c in unneeded_cols if c in chunk.columns]
        chunk = chunk.drop(columns=cols_to_drop)
        
        #Rename Columns if they are in the chunk
        rename_exists = {k: v for k, v in rename_cols.items()if k in chunk.columns}
        chunk = chunk.rename(columns=rename_exists)

        #For the first chunk write with header
        if i == 0:
            chunk.to_csv(output, index=False)
            if rename_exists:
                logger.info(f"Renamed columns: {list(rename_exists.values())}")
        #Ignore header for rest of the chunks
        else:
            chunk.to_csv(output, mode='a', index=False, header=False)

    logger.info(f"Dropped {len(unneeded_cols)} columns from raw data")
