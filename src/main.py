'''Main'''
import logging
from pathlib import Path
from logger.logging_config import log_setup
from pipeline import run_pipeline

BASEPATH = Path(__file__).resolve().parent.parent
RAWDATA = BASEPATH / "data" / "nfl_play_by_play.csv"
CLEANED = BASEPATH / "data" / "nfl_play_by_play_cleaned.csv"

def main():
    '''Main'''
    logger = logging.getLogger(__name__)
    logger.info("Starting Pipeline")
    logger.info(f"Input File: {RAWDATA}")
    try:
        run_pipeline(RAWDATA, CLEANED)
    finally:
        logger.info("Finished Pipeline \n")


if __name__ == "__main__":
    log_setup()
    main()
