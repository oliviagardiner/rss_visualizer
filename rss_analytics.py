import csv
import os
from pathlib import Path

ABS_PATH = os.path.dirname(__file__)

class RssAnalytics:
    def __init__(self, stat_dirname = 'daily_statistics', abs_path = None):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.stat_filepath = stat_dirname
        self.init_rss_analytics_paths()

    def init_rss_analytics_paths(self):
        """Changes the path of the statistics directory to absolute paths. Creates the directory if it doesn't exist.
        """
        self.stat_filepath = os.path.join(self.abs_path, self.stat_filepath)
        Path(self.stat_filepath).mkdir(parents=True, exist_ok=True)
    
# WIP