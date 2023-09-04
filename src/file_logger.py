#!/usr/bin/python3

from src.file_util import FileUtil
import logging
from io import StringIO
from datetime import date

class FileLogger():
    POSTFIX = '_log'

    LEVEL_INFO = 'info'
    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'

    def __init__(self, filename: str = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if filename:
            self.__configure_file_handler(formatter, filename)

        self.__configure_stream_handler(formatter)

    def __configure_file_handler(self, formatter, filename: str) -> None:
        fileutil = FileUtil()
        path = fileutil.make_gen_path('logs')
        filename = date.today().strftime('%Y-%m-%d') + '-' + filename + self.POSTFIX
        file_handler = logging.FileHandler(path + '/' + filename)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def __configure_stream_handler(self, formatter) -> None:
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
