import os
import urllib.request
from urllib.error import HTTPError
from datetime import datetime, date
from src.rss_processor import RssProcessor

ABS_PATH = os.path.dirname(__file__)

class RssDownloader(RssProcessor):
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None, log_dirname = 'rss_logs', logger_name = __name__):
        RssProcessor.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

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
