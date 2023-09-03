#!/usr/bin/python3

import logging
import os
from io import StringIO

ABS_PATH = os.path.dirname(__file__)

class FileLogger():
    GEN_DIR = '../generated/'

    LEVEL_INFO = 'info'
    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'

    def __init__(self, filename: str = None, is_abs: bool = False) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if is_abs == True:
            filename = os.path.join(ABS_PATH, self.GEN_DIR + filename)
        

        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self.stream = StringIO()
        stream_handler = logging.StreamHandler(self.stream)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def log(self, message: str, level = 'info') -> None:
        if level == self.LEVEL_WARNING:
            self.logger.warning(message)
        elif level == self.LEVEL_ERROR:
            self.logger.error(message)
        else:
            self.logger.info(message)
