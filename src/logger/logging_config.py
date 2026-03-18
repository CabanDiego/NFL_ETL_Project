'''Module to set up logger'''
import logging
from pathlib import Path

def log_setup():
    '''Logger set up'''

    #Creating location for the logs file
    log_dir = Path(__file__).resolve().parent
    
    log_file = log_dir / "logs.log"
    
    #Configuring the log to info, create or append to the log file, and return time and message
    logging.basicConfig(filename=str(log_file), 
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s- %(message)s')