#!/usr/bin/python3.7

import urllib.request
from urllib.error import HTTPError
from datetime import datetime, date
from pathlib import Path
import json
import os

ABS_PATH = os.path.dirname(__file__)

class RssDownloader:

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.today = today
        self.config_filepath = json_filename
        self.download_filepath = download_dirname
        self.init_rss_downloader_paths()

    def init_rss_downloader_paths(self):
        """Changes the path of the download directory and the json config to absolute paths. Creates the download directory if it doesn't exist.
        """
        self.config_filepath = os.path.join(self.abs_path, self.config_filepath)
        self.download_filepath = os.path.join(self.abs_path, self.download_filepath + '/' + self.today)
        Path(self.download_filepath).mkdir(parents=True, exist_ok=True)

    def convert_json_to_dict(self):
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
    
    def log_error(self, err, url):
        """Saves the error message and timestamp in log.txt in the downloads folder."""
        msg =  self.format_date() + ' Error trying to download file from url: [' + url + '] ' + str(err.code) + ': ' + str(err.reason)
        f = open(self.download_filepath + '/log.txt', 'a+')
        f.write(msg + '\n')
        f.close()

    def rss_file_path_for(self, key):
        return self.download_filepath  + '/' + self.format_date() + '_' + key + '_rss.xml'

    def run(self):
        """Some servers will reject your request if the User-Agent header is not set
        so we make a 2nd attempt if the first try throws a 403 (Forbidden) error code.
        """
        urls = self.convert_json_to_dict()

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
                        self.log_error(err, val)
                else:   
                    self.log_error(err, val)
