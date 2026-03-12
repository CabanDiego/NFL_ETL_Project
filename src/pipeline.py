'''Module to run the pipeline'''
import logging
from pathlib import Path
from manage_csv.csv_mngr import manage_file

logger = logging.getLogger(__name__)

def run_pipeline(source: Path, outpath: Path):
    '''Run Pipeline'''
    manage_file(source, outpath)
    