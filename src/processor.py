#!/usr/bin/python3

from src.file_logger import FileLogger
from src.file_util import FileUtil
from src.config_parser import ConfigParser
from src.downloader import Downloader
from datetime import datetime
from dotenv import load_dotenv
import os

class Processor():
    POSTFIX = '_rss.xml'

    def __init__(self, config_path: str) -> None:
        load_dotenv()
        self.logger = FileLogger('default')
        self.config_parser = ConfigParser(config_path)
        self.urls = self.config_parser.get_values_by_key('url')
        
    def get_rss_for_urls(self) -> None:
        file_util = FileUtil()
        now = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        downloader = Downloader()

        for key, val in self.urls.items():
            if val:
                try:
                    data = downloader.get_data(val)
                    path = file_util.make_gen_path(
                        os.getenv('RSS_SUBDIR'))
                    file_util.save_to_path(
                        data, path + '/' + now + '_' + key + self.POSTFIX)
                    self.logger.log('File downloaded for key: ' + key)
                except Exception as err:
                    self.logger.log(
                        'Unable to save file for key: ' + key, self.logger.LEVEL_ERROR)
            else:
                self.logger.log('No url was specified for key: ' + key, self.logger.LEVEL_WARNING)
