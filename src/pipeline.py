'''Module to run the pipeline'''
import logging
from pathlib import Path
from manage_csv.extract import read_and_load
from manage_csv.load_into_db import load_to_db
from sql.run_sql import run_sql_file

logger = logging.getLogger(__name__)

def run_pipeline(source: Path, db_url:str):
    '''Run Pipeline'''
    chunks = read_and_load(source)
    
    load_to_db(chunks, db_url)
    
    run_sql_file(db_url, Path("src/sql/create_tables.sql"))
    
    run_sql_file(db_url, Path("src/sql/insert_into_tables.sql"))
