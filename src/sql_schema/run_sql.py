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
    
    #Starting the engine as a connection to use sql commands
    with engine.begin() as conn:
        #Try block to read .sql files and run them inside the db
        try:
            sql_commands = sql_path.read_text()
            conn.execute(text(sql_commands))
        except Exception as e:
            logger.error(f"Exception: {e} when running SQL file: {sql_path}")
        
    logger.info(f"Finished running SQL file: {sql_path}")