#!/usr/bin/python3

from src.file_logger import FileLogger
import urllib.request
import ssl
import sys
from urllib.error import URLError

sys.path.append('.')

class Downloader():
    def __init__(self) -> None:
        self.logger = FileLogger('default')

    def get_data(self, url: str) -> str:
        context = ssl._create_unverified_context()
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'}
        
        try:
            req = urllib.request.Request(url, headers=header)
            response = urllib.request.urlopen(req, context=context)
            if (response.getcode() == 200):
                return response.read()
            else:
                raise Exception('Error while opening url: ' + url)
        except URLError as err:
            self.logger.log(
                'Error trying to download file from url: [' + url + '] ' + ': ' + str(err.reason), FileLogger.LEVEL_WARNING)