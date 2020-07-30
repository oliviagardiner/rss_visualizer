#!/usr/bin/python3

import os
import urllib.request
import ssl
from urllib.error import URLError
from datetime import datetime, date
from .rss_processor import RssProcessor

ABS_PATH = os.path.dirname(__file__)

class RssDownloader(RssProcessor):
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_config.json', download_dirname = 'rss_downloads', abs_path = None, log_dirname = 'rss_logs', logger_name = __name__):
        RssProcessor.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

    def run(self):
        """Some servers will reject your request if the User-Agent header is not set
        so we make a 2nd attempt if the first try throws a 403 (Forbidden) error code.
        """
        urls = self.get_config()
        context = ssl._create_unverified_context()
        header = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0' }

        for key, val in urls.items():
            try:
                req = urllib.request.Request(val, headers = header)
                response = urllib.request.urlopen(req, context=context)
                if (response.getcode() == 200):
                    data = response.read()
                    filepath = open(self.rss_file_path_for(key), 'wb')
                    filepath.write(data)
                else:
                    raise Exception('Error while opening url: ' + val)
            except URLError as err:
                self.logger.warning('Error trying to download file from url: [' + val + '] ' + ': ' + str(err.reason))
        self.logger.info('RSS feed download finished, time elapsed: ' + self.get_time_elapsed())
