import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def read_file(source: Path):
    chunk_size = 50000
    logger.info("Test")
    print("Test")