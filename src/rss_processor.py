import json
import os
import glob
import logging
import time
from datetime import datetime, date
from pathlib import Path
from xml.dom import minidom
from xml.dom.minidom import Node

ABS_PATH = os.path.dirname(__file__)

class RssProcessor:
    gen_dir = '../generated/'

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None, log_dirname = 'rss_logs', logger_name = __name__):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.today = today
        self.config_filepath = json_filename
        self.download_filepath = download_dirname
        self.logging_filepath = log_dirname
        self.logger_name = logger_name
        self.init_paths()
        self.setup_log()

    def init_paths(self):
        """Changes the path of the download directory and the json config to absolute paths. Creates the download directory if it doesn't exist.
        """
        self.config_filepath = os.path.abspath(os.path.join(self.abs_path, '../' + self.config_filepath))
        self.download_filepath = self.convert_to_abs_path(self.download_filepath + '/' + self.today, is_dir = True)
        self.logging_filepath = self.convert_to_abs_path(self.logging_filepath, is_dir = True)
    
    def convert_to_abs_path(self, path, is_dir = False):
        p = os.path.join(self.abs_path, self.gen_dir + path)
        if is_dir is True:
            Path(p).mkdir(parents = True, exist_ok = True)
        return p

    def setup_log(self):
        """Creates a logging object that can be used by child classes.
        """
        self.start = time.time()
        logging.basicConfig(filename = self.logging_filepath + '/' + self.today + '_rss_log.txt', level = logging.DEBUG, format = '%(asctime)s %(name)s %(levelname)s %(message)s', datefmt ='%Y-%m-%d %I:%M:%S ')
        self.logger = logging.getLogger(self.logger_name)
        self.logger.info('Module started')

    def is_config_valid(self):
        try:
            with open(self.config_filepath) as json_file:
                json.load(json_file)
        except ValueError as e:
            self.logger.warning('The config file is NOT a valid json - %s'%(e))
            return False
        self.logger.info('The config file not a valid json')
        return True

    def get_config(self, domains_only = True):
        """Converts the json config file for the rss feeds into a uid-url dictionary.

        Returns
        ---
        dictionary
        """
        urls = dict()
        fields = dict()
        if self.is_config_valid() is True:
            with open(self.config_filepath) as json_file:
                data = json.load(json_file)
                for key in data['feeds']:
                    urls[key] = data['feeds'].get(key, '').get('domain', '')
                    fields[key] = data['feeds'].get(key, '').get('fields', None)
        if domains_only is True:
            return urls
        else:
            return urls, fields

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

    def get_text_by_tag(self, tag, key, allow_duplicates = False):
        """Collects all text from a specified tag per key per day and returns it as one long string.

        Returns
        ---
        string
        """
        if allow_duplicates is True:
            text = []
        else:
            text = set()

        filelist = self.get_file_list(key)
        
        for filename in filelist:
            doc = minidom.parse(filename)
            items = doc.getElementsByTagName('item')

            for elem in items:
                for child in elem.childNodes:
                    if (child.nodeType == Node.ELEMENT_NODE and child.tagName == tag and child.hasChildNodes() == True):
                        if allow_duplicates is True:
                            text.append(child.firstChild.data.strip())
                        else:
                            text.add(child.firstChild.data.strip())

        return ' '.join(text)

    def run(self):
        self.logger.info('Module finished, time elapsed: ' + self.get_time_elapsed())
        

