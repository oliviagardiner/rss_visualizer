#!/usr/bin/python3

from src.file_logger import FileLogger
from src.file_util import FileUtil
from src.downloader import Downloader
from datetime import datetime
from dotenv import load_dotenv
import os
import json

class Processor():
    POSTFIX = '_rss.xml'

    def __init__(self, config_path: str) -> None:
        load_dotenv()
        self.logger = FileLogger('default')
        self.file_util = FileUtil()
        self.config_path = self.file_util.get_abs_path(config_path)
        self.urls = self.__load_urls_from_config()

    def __load_urls_from_config(self) -> dict:
        urls = dict()

        try:
            with open(self.config_path) as json_file:
                data = json.load(json_file)
                for key in data['feeds']:
                    urls[key] = data['feeds'].get(key, '').get('url', '')
        except ValueError as e:
            self.logger.log(
                'The config file is NOT a valid json - %s' % (e), self.logger.LEVEL_WARNING)
        finally:
            self.logger.log('Urls loaded from config.')
            return urls
        
    def get_rss_for_urls(self) -> None:
        now = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        downloader = Downloader()

        for key, val in self.urls.items():
            if val:
                try:
                    data = downloader.get_data(val)
                    path = self.file_util.make_gen_path(
                        os.getenv('RSS_SUBDIR'))
                    self.file_util.save_to_path(
                        data, path + '/' + now + '_' + key + self.POSTFIX)
                    self.logger.log('File downloaded for key: ' + key)
                except Exception as err:
                    self.logger.log(
                        'Unable to save file for key: ' + key, self.logger.LEVEL_ERROR)
            else:
                self.logger.log('No url was specified for key: ' + key, self.logger.LEVEL_WARNING)
