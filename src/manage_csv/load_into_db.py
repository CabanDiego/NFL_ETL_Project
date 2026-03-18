'''Send chunks into db'''
import logging
import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def load_to_db(df_chunks, db_url: str)-> None:
    '''Connect to Postgres and send chunks to table'''
    #Create engine to connect to the database
    engine = create_engine(db_url, connect_args={"connect_timeout": 10})
    #Create table name for the raw data
    table_name = "nfl_pbp_raw"
    
    logger.info(f"Loading chunks into initial db table")
    
    #Set first chunk to true to read it in as first chunk
    first_chunk = True  
    for chunk in df_chunks:
        try:
            #Lowercase all columns for easier use in db
            chunk.columns = [c.lower() for c in chunk.columns]
            #Convert Date column to datetime
            if 'date' in chunk.columns:
                chunk['date'] = pd.to_datetime(chunk['date'])
                #Sending each chunk to the db and checking if the current chunk is the first
            chunk.to_sql(
                table_name,
                engine,
                #Create table on the first chunk, otherwise append to the table
                if_exists='replace' if first_chunk else 'append',  
                index=False,
                method='multi'
            )
            #After first chunk set it equal to false so rest of chunks are not recognized as first chunk
            first_chunk = False
        except Exception as e:
            logger.error(f"Failed to load chunk: {e}")