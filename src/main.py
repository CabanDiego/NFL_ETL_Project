'''Main'''
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from logger.logging_config import log_setup
from pipeline import run_pipeline

#Saving dataset location
BASEPATH = Path(__file__).resolve().parent.parent
RAWDATA = BASEPATH / "data" / "nfl_play_by_play.csv"
load_dotenv()

#URL for DB in EC2
db_url = (
    f"postgresql+psycopg2://{os.environ['PG_USER']}:"
    f"{os.environ['PG_PASS']}@{os.environ['PG_HOST']}:5432/"
    f"{os.environ['PG_DB']}"
)

def main():
    '''Main'''
    logger = logging.getLogger(__name__)
    logger.info("Starting Pipeline")
    logger.info(f"Input File: {RAWDATA}")
    try:
        run_pipeline(RAWDATA, db_url)
    except Exception as e:
        logger.exception("Pipeline Failed")
    finally:
        logger.info("Finished Pipeline \n")


if __name__ == "__main__":
    log_setup()
    main()
