#!/usr/bin/python3

import csv
import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from pathlib import Path
from .rss_processor import RssProcessor

ABS_PATH = os.path.dirname(__file__)

class RssAnalytics(RssProcessor):
    
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_config.json', download_dirname = 'rss_downloads', abs_path = None,log_dirname = 'rss_logs', logger_name = __name__, tag = '', stat_dirname = 'rss_statistics', csv_filename = 'data.csv'):
        RssProcessor.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

        self.stat_filepath = self.convert_to_abs_path(stat_dirname, is_dir = True)
        self.csv_filepath = self.convert_to_abs_path(stat_dirname + '/' + self.today + '_' + csv_filename)
        self.last_week = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.digest_filepath = self.convert_to_abs_path(
            stat_dirname + '/' + self.last_week + '_' + 'digest.txt')
        
    def get_last_week_digest(self):
        data = pd.read_csv(self.csv_filepath, index_col='pkey',
                           sep=';', parse_dates=['pubDate'])
        data.info()
        filter = data.loc[(data['pubDate'] >= self.last_week)].sort_values('pubDate')
        digest = ''
        for index, row in filter.iterrows():
            settings = self.get_config_feed(row['key'])
            urls = ''
            for key, value in settings['links'].items():
                urls += '[' + key.capitalize() + '](' + value + ') '
            digest += row['title'] + '\r\n' + 'Csatorna: ' + settings['name'] + '\r\n' + 'Megjelenik: ' + str(settings['published']) + '\r\n' + 'Linkek: ' + urls + '\r\n' + str(row['description']) + '\r\n---\r\n'
            
        return digest
    
    def get_last_week_digest_as_markdown(self):
        data = pd.read_csv(self.csv_filepath, index_col='pkey',
                           sep=';', parse_dates=['pubDate'])
        data.info()
        filter = data.loc[(data['pubDate'] >= self.last_week)
                          ].sort_values('pubDate')
        digest = ''
        for index, row in filter.iterrows():
            settings = self.get_config_feed(row['key'])
            urls = ''
            for key, value in settings['links'].items():
                urls += '[' + key.capitalize() + '](' + value + ') '
            title = '### ' + row['title']
            channel = 'Csatorna: **' + settings['name'] + '**'
            published = 'Megjelenik: ' + str(settings['published'])
            links = 'Linkek: ' + urls
            digest += title + '\r\n' + channel + '\n' + published + '\n' + links + '\r\n' + str(row['description']) + '\r\n---\r\n'

        return digest
    
    def write_digest_file(self, data):
        try:
            file = open(self.digest_filepath, 'x', encoding='utf-8')
        except FileExistsError as err:
            file = open(self.digest_filepath, 'w', encoding='utf-8')

        try:
            file.write(data)
            file.close()
        except IOError as err:
            self.logger.error(
                'Error trying to write data to file: [' + self.digest_filepath + '] ' + ': ' + str(err.reason))
    
    def run(self):
        digest = self.get_last_week_digest_as_markdown()
        self.write_digest_file(digest)
        self.logger.info('Digest generated: ' + self.digest_filepath)
