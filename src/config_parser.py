#!/usr/bin/python3

from src.file_util import FileUtil
import json

class ConfigParser():
    def __init__(self, config_path: str) -> None:
        self.file_util = FileUtil()
        self.config_path = self.file_util.get_abs_path(config_path)

    def get_values_by_key(self, select_key: str):
        values = dict()

        try:
            with open(self.config_path, encoding='utf-8') as json_file:
                data = json.load(json_file)
                for key in data['feeds']:
                    values[key] = data['feeds'].get(
                        key, '').get(select_key, '')
                
                return values
        except ValueError as e:
            raise Exception('The config file is NOT a valid json.')
        
    def get_settings_for_feed_key(self, key: str):
        try:
            with open(self.config_path, encoding='utf-8') as json_file:
                data = json.load(json_file)
                return data['feeds'].get(key, None)
        except ValueError as e:
            raise Exception('The config file is NOT a valid json.')
