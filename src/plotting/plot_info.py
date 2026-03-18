'''Module for plotting'''
from pathlib import Path
import logging
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

#Creating a new directory to store the graphs
BASEPATH = Path(__file__).resolve().parent.parent.parent
OUTDIR = BASEPATH / "output_graphs" 

logger = logging.getLogger(__name__)

def get_facts(db_url:str)-> pd.DataFrame:
    '''Retrieves from the Facts table in the database'''
    #Query to retrieve facts
    sql_query = text('''SELECT * FROM total_team_facts ORDER BY season, posteam''')
    
    #Creating and running an engine as a connection
    engine = create_engine(db_url)
    
    try:
        #Connecting with the engine
        with engine.connect() as conn:
            logger.info("Attempting to retrieve facts from the database")
            #Executing select query
            result = conn.execute(sql_query)
            #Saving the results into a dataframe
            df = pd.DataFrame(result.fetchall(), columns=list(result.keys()))
            logger.info('Successfully retrieved facts from the database')
            return df
    except Exception as e:
        logger.error(f"Exception {e} when retrieving facts from database")
        raise
    
    
def plot_facts(df: pd.DataFrame)-> None:
    '''Plots facts from the database'''
    if df.empty:
        logger.warning("Facts dataframe is empty")
        raise ValueError("Facts DataFrame is Empty")
    
    #Creating new directory for the graphs if it doesnt exist
    OUTDIR.mkdir(parents=True, exist_ok=True)
    try:
        logger.info("Plotting team statistics by season")
        #Getting each unique season
        seasons = sorted(df['season'].unique())
        
        #Looping through each season's data and sorting teams based on positive run percentage
        for season in seasons:
            season_df = df[df['season'] == season].sort_values(
                by='pos_run', ascending=False
            )
            
            #Converting wanted columns to lists
            teams = list(season_df['posteam'])
            pos_run = list(season_df['pos_run'])
            pos_pass = list(season_df['pos_pass'])
            
            #Positions along the x-axis for each team
            x = range(len(teams))
            
            #Width of the bars
            width = 0.35  
            
            #Creates figure for each season
            plt.figure(figsize=(12, 6))
            
            #Plotting 2 bars per team for each stat
            plt.bar([i - width/2 for i in x], pos_run, width=width, label='Positive Run %', color='blue')
            plt.bar([i + width/2 for i in x], pos_pass, width=width, label='Positive Pass %', color='red')
            
            #Setting labels and rotating the graph
            plt.xticks(ticks=x, labels=teams, rotation=90)
            plt.ylim(0, 100)
            plt.xlabel("Team")
            plt.ylabel("Percentage")
            plt.title(f"Positive Run and Pass Percentage by Team - Season {season}")
            plt.legend()
            plt.tight_layout()
            
            #Saving each graph to the directory/folder
            file_path = OUTDIR / f"pos_run_pass_season_{season}.png"
            plt.savefig(file_path)
            plt.close()
            
            logger.info(f"Graph created for {season} season")
        
    except Exception as e:
        logger.error(f"Exception while plotting data: {e}")
        raise