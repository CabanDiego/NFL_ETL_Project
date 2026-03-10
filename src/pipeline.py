'''Module to run the pipeline'''
import logging
from pathlib import Path
from read_data.read import read_file

logger = logging.getLogger(__name__)

def run_pipeline(source: Path):
    '''Run Pipeline'''
    read_file(source)
    