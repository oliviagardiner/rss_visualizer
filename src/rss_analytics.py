#!/usr/bin/python3

import csv
import os
import pandas
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from pathlib import Path
from rss_processor import RssProcessor

ABS_PATH = os.path.dirname(__file__)

class RssAnalytics(RssProcessor):
    
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_config.json', download_dirname = 'rss_downloads', abs_path = None,log_dirname = 'rss_logs', logger_name = __name__, tag = '', stat_dirname = 'rss_statistics', csv_filename = 'data.csv'):
        RssProcessor.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

        self.stat_filepath = self.convert_to_abs_path(stat_dirname, is_dir = True)
        self.csv_filepath = self.convert_to_abs_path(stat_dirname + '/' + self.today + '_' + csv_filename)
    
    def run(self):
        pass
        # data = pandas.read_csv(self.csv_filepath, index_col = 'pkey', header = 0, sep = ';')
        # WIP
