'''Send chunks into db'''
import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def load_to_db(df_chunks, db_url: str):
    '''Connect to Postgres and send chunks to table'''
    engine = create_engine(db_url, connect_args={"connect_timeout": 10})
    table_name = "nfl_pbp_raw"
    
    logger.info(f"Loading chunks into initial db table")
    for chunk in df_chunks:
        try:
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
        except Exception as e:
            logger.error(f"Failed to load chunk: {e}")