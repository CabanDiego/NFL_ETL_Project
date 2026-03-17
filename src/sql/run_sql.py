'''Run SQL Files helper'''
from pathlib import Path
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

def run_sql_file(db_url: str, sql_path: Path):
    """Execute a SQL file on PostgreSQL"""
    logger.info(f"Running SQL file: {sql_path}")
    engine = create_engine(db_url)
    
    with engine.begin() as conn: 
        sql_commands = sql_path.read_text()
        conn.execute(text(sql_commands))
        
    logger.info(f"Finished running SQL file: {sql_path}")