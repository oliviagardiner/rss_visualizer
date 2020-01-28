import csv
import os
import pandas
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from pathlib import Path
from rss_downloader import RssDownloader

ABS_PATH = os.path.dirname(__file__)

class RssAnalytics(RssDownloader):
    
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None,logfile = 'rss_logs.txt', stat_dirname = 'daily_statistics', csv_filename = 'data.csv'):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.today = today
        self.config_filepath = json_filename
        self.download_filepath = download_dirname
        self.logging_filepath = logfile
        self.init_rss_downloader_paths()

        self.stat_filepath = stat_dirname
        self.csv_filepath = 'data.csv'
        self.init_rss_analytics_paths()

    def init_rss_analytics_paths(self):
        """Changes the path of the statistics directory to absolute paths. Creates the directory if it doesn't exist.
        """
        self.stat_filepath = os.path.join(self.abs_path, self.stat_filepath)
        self.csv_filepath = os.path.join(self.stat_filepath, self.today + '_' + self.csv_filepath)
        Path(self.stat_filepath).mkdir(parents=True, exist_ok=True)
    
    def run(self):
        data = pandas.read_csv(self.csv_filepath, index_col = 'pkey', header = 0, sep = ';')