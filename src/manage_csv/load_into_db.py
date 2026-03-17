'''Send chunks into db'''
import logging
import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def load_to_db(df_chunks, db_url: str):
    '''Connect to Postgres and send chunks to table'''
    engine = create_engine(db_url, connect_args={"connect_timeout": 10})
    table_name = "nfl_pbp_raw"
    
    logger.info(f"Loading chunks into initial db table")
    
    #See if it is the first chunk
    first_chunk = True  
    for chunk in df_chunks:
        try:
            chunk.columns = [c.lower() for c in chunk.columns]
            #Convert Date column to datetime
            if 'date' in chunk.columns:
                chunk['date'] = pd.to_datetime(chunk['date'])
            chunk.to_sql(
                table_name,
                engine,
                #Create table on the first chunk
                if_exists='replace' if first_chunk else 'append',  
                index=False,
                method='multi'
            )
            first_chunk = False
        except Exception as e:
            logger.error(f"Failed to load chunk: {e}")