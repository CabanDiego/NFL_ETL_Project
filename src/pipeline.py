'''Module to run the pipeline'''
import logging
from pathlib import Path
from manage_csv.extract import read_and_load
from manage_csv.load_into_db import load_to_db

logger = logging.getLogger(__name__)

def run_pipeline(source: Path, db_url:str):
    '''Run Pipeline'''
    chunks = read_and_load(source)
    
    load_to_db(chunks, db_url)
