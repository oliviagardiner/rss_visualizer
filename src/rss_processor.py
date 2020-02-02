import glob
import json
import logging
import os
import re
import shutil
import time
from datetime import datetime, date
from pathlib import Path
from xml.dom import minidom
from xml.dom.minidom import Node

ABS_PATH = os.path.dirname(__file__)

class RssProcessor:
    gen_dir = '../generated/'

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_config.json', download_dirname = 'rss_downloads', abs_path = None, log_dirname = 'rss_logs', logger_name = __name__):
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
        self.archive_filepath = self.convert_to_abs_path('rss_archive', is_dir = True)
    
    def convert_to_abs_path(self, path, is_dir = False):
        """Returns the absolute path of a filename, if the path is a directory, this will also attempt to create it.

        Returns
        ---
        string
        """
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
        """Checks if the config file is a valid json and logs the result.

        Returns
        ---
        boolean
        """
        try:
            with open(self.config_filepath) as json_file:
                json.load(json_file)
        except ValueError as e:
            self.logger.warning('The config file is NOT a valid json - %s'%(e))
            return False
        self.logger.info('The config file is a valid json')
        return True

    def get_config(self, urls_only = True):
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
                    urls[key] = data['feeds'].get(key, '').get('url', '')
                    fields[key] = data['feeds'].get(key, '').get('fields', None)
        if urls_only is True:
            return urls
        else:
            return urls, fields
    
    def get_config_settings(self, key):
        """Extracts the value of a specific setting from the json config, returns None if not found.

        Returns
        ---
        mixed
        """
        if self.is_config_valid() is True:
            with open(self.config_filepath) as json_file:
                data = json.load(json_file)
                return data['settings'][key] or None

    def clean_html(self, text):
        """This will remove everything that is enclosed in a html tag. It was handy to clean up the XMLs because some of the RSS feeds I used for testing incorrectly enclosed HTML inside certain XML tags.

        Returns
        ---
        string
        """
        cl = re.compile('<.*?>')
        cl_text = re.sub(cl, '', str(text))
        cl_text = cl_text.strip()
        cl_text = cl_text.replace('\n', '')
        cl_text = cl_text.replace('\t', '')
        return cl_text

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
            enclosing_tag = self.get_config_settings('enclosing_tag_name') if isinstance(self.get_config_settings('enclosing_tag_name'), str) else 'item'
            items = doc.getElementsByTagName(enclosing_tag)

            for elem in items:
                for child in elem.childNodes:
                    if (child.nodeType == Node.ELEMENT_NODE and child.tagName == tag and child.hasChildNodes() == True):
                        value = self.clean_html(child.firstChild.data) or ''
                        if allow_duplicates is True:
                            text.append(value)
                        else:
                            text.add(value)

        return ' '.join(text)

    def archive_folder(self, path, day = None):
        """Compresses a folder's contents.
        """
        day = day + '-' if day != None else ''
        target = self.archive_filepath + '/' + day + 'rss_archive'
        shutil.make_archive(target, 'zip', path)
    
    def archive_day(self, day):
        """Archives the raw XML files of a certain day and then removes the original uncompressed folder and its contents.
        """
        xml_cleanup = self.get_config_settings('xml_cleanup') if isinstance(self.get_config_settings('xml_cleanup'), bool) else False
        if xml_cleanup is True:
            path = os.path.abspath(self.download_filepath + '/../' + day)
            if os.path.isdir(path):
                self.logger.info('Target path is an existing directory, archiving and removing: ' + path)
                try:
                    self.archive_folder(path, day)
                    self.logger.info('Successfully archived: ' + path)
                except:
                    self.logger.warning('Error while trying to archive path: ' + path)

                try:
                    shutil.rmtree(path)
                    self.logger.info('Successfully deleted: ' + path)
                except:
                    self.logger.warning('Error while trying to delete path: ' + path)
            else:
                self.logger.info('Target path is not an existing directory, nothing to archive: ' + path)
        else:
            self.logger.info('XML cleanup is disabled in the settings')

    def run(self):
        self.logger.info('Module finished, time elapsed: ' + self.get_time_elapsed())
