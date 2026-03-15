from pathlib import Path
from sqlalchemy import create_engine
import os
import sys

#Using the root to find extract.py since it is in a different folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.manage_csv.extract import read_and_load

DATA_FILE = Path("data/nfl_play_by_play.csv")
DB_PATH = Path("test/sandbox.db")
TABLE_NAME = "plays"

#Refres the .db file
if DB_PATH.exists():
    os.remove(DB_PATH)
    print("Deleted old sandbox.db")

#SQLite engine
engine = create_engine(f"sqlite:///{DB_PATH}")

#Load chunks using my method from extract.py
for i, chunk in enumerate(read_and_load(DATA_FILE)):
    chunk.to_sql(TABLE_NAME, engine, index=False, if_exists='append')
