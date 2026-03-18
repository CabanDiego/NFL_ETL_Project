'''Module to run the pipeline'''
import logging
from pathlib import Path
import pandas as pd
from manage_csv.extract import read_and_load
from manage_csv.load_into_db import load_to_db
from sql_schema.set_up_tables import run_sql_file
from plotting.plot_info import get_facts, plot_facts

logger = logging.getLogger(__name__)

def run_pipeline(source: Path, db_url:str) -> None:
    '''Run Pipeline'''
    chunks = read_and_load(source)
    
    #Loading dataset into staging on the PostgreSQL DB
    load_to_db(chunks, db_url)
    
    #Running .sql files inside the db
    logger.info("Creating tables inside the data warehouse")
    run_sql_file(db_url, Path("src/sql_schema/create_tables.sql"))
    
    logger.info("Populating tables inside data warehouse using raw table in staging")
    run_sql_file(db_url, Path("src/sql_schema/insert_into_tables.sql"))

    #Retrieving info and plotting it
    logger.info("Querying the database to plot information")
    df = get_facts(db_url)
    
    logger.info("Plotting facts")
    plot_facts(df)
