import urllib.request
from urllib.error import HTTPError
from datetime import datetime, date
from pathlib import Path
import json
import os
import glob
import logging
import time

ABS_PATH = os.path.dirname(__file__)

class RssDownloader:
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None, log_dirname = 'rss_logs', logger_name = __name__):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.today = today
        self.config_filepath = json_filename
        self.download_filepath = download_dirname
        self.logging_filepath = log_dirname
        self.logger_name = logger_name
        self.init_rss_downloader_paths()
        self.setup_log()

    def init_rss_downloader_paths(self):
        """Changes the path of the download directory and the json config to absolute paths. Creates the download directory if it doesn't exist.
        """
        self.config_filepath = os.path.join(self.abs_path, self.config_filepath)
        self.download_filepath = os.path.join(self.abs_path, self.download_filepath + '/' + self.today)
        self.logging_filepath = os.path.join(self.abs_path, self.logging_filepath)
        Path(self.download_filepath).mkdir(parents=True, exist_ok=True)
        Path(self.logging_filepath).mkdir(parents=True, exist_ok=True)

    def setup_log(self):
        """Creates a logging object that can be used by child classes.
        """
        self.start = time.time()
        logging.basicConfig(filename = self.logging_filepath + '/' + self.today + '_rss_log.txt', level = logging.DEBUG, format = '%(asctime)s %(name)s %(levelname)s %(message)s', datefmt ='%Y-%m-%d %I:%M:%S ')
        self.logger = logging.getLogger(self.logger_name)
        self.logger.info('Module started')

    def get_config(self):
        """Converts the json config file for the rss feeds into a uid-url dictionary.

        Returns
        ---
        dictionary
        """
        urls = dict()
        with open(self.config_filepath) as json_file:
            data = json.load(json_file)
            for key in data['feeds']:
                urls[key] = data['feeds'].get(key, '').get('domain', '')
        return urls

    def format_date(self):
        """Returns the formatted string of the current time as YYYY-mm-dd-HHiiss.

        Returns
        ---
        string
        """
        now = datetime.now()
        return now.strftime('%Y-%m-%d-%H%M%S')

    def rss_file_path_for(self, key):
        """Returns the XML file path by date and key.
        
        Returns
        ---
        string
        """
        return self.download_filepath  + '/' + self.format_date() + '_' + key + '_rss.xml'
    
    def get_file_list(self, key):
        """Returns a list of file paths that match the requirements (uid and timestamp).

        Returns
        ---
        list
        """
        pattern = self.today + '-*_' + key + '_rss.xml'
        pattern = os.path.join(self.download_filepath, pattern)
        
        return glob.glob(pattern)

    def get_time_elapsed(self):
        """Gets the running time elapsed since the object was initiated in seconds.
        Returns
        ---
        string
        """
        return str(time.time() - self.start) + 's'

    def run(self):
        """Some servers will reject your request if the User-Agent header is not set
        so we make a 2nd attempt if the first try throws a 403 (Forbidden) error code.
        """
        urls = self.get_config()

        for key, val in urls.items():
            try:
                urllib.request.urlretrieve(val, self.rss_file_path_for(key))
            except HTTPError as err:
                if err.code == 403:
                    try:
                        opener = urllib.request.URLopener()
                        opener.addheader('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0')
                        opener.retrieve(val, self.rss_file_path_for(key))
                    except HTTPError as err:
                        self.logger.warning('Error trying to download file from url: [' + val + '] ' + str(err.code) + ': ' + str(err.reason))
                else:
                    self.logger.warning('Error trying to download file from url: [' + val + '] ' + str(err.code) + ': ' + str(err.reason))
        self.logger.info('RSS feed download finished, time elapsed: ' + self.get_time_elapsed())
        

