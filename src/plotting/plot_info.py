'''Module for plotting'''
from pathlib import Path
from typing import List
import logging
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

def get_facts(db_url:str, sql_path)-> pd.DataFrame:
    '''Retrieves from the Facts table in the database'''
    #Creating and running an engine as a connection
    engine = create_engine(db_url)
    with engine.begin() as conn:
        #Try block to read sql file for queries
        try:
            sql_commands = sql_path.read_text()
            conn.execute(text(sql_commands))
        except Exception as e:
            logger.error(f"Exception: {e} when running SQL file: {sql_path}")

def plot_facts(df: pd.Dataframe)-> None:
    '''Plots facts from the database'''
    return None