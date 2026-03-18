'''Run SQL Files helper'''
from pathlib import Path
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

def run_sql_file(db_url: str, sql_path: Path) -> None:
    """Execute a SQL file on PostgreSQL"""
    logger.info(f"Running SQL file: {sql_path}")
    
    #Creating engine to connect to db to run sql files
    engine = create_engine(db_url)
    
    try:
        #Read whole sql file as a string
        sql_commands = sql_path.read_text()
        #Use raw connection to do multiple statements
        with engine.raw_connection() as conn:
            cursor = conn.cursor()
            try:
                #Execute statements
                cursor.execute(sql_commands)
            finally:
                #Close the cursor
                cursor.close()
                #Commit the statements
            conn.commit()
    except Exception as e:
        logger.error(f"Exception: {e} when running SQL file: {sql_path}")
        raise
        
    logger.info(f"Finished running SQL file: {sql_path}")