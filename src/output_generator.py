#!/usr/bin/python3

from src.file_logger import FileLogger
from src.config_parser import ConfigParser
from src.file_util import FileUtil
import pandas as pd
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
import os

class OutputGenerator():
    def __init__(self, config_path: str, day: str = date.today().strftime('%Y-%m-%d')) -> None:
        load_dotenv()
        self.logger = FileLogger('default')
        self.file_util = FileUtil()
        self.fields = self.__get_fields_list()
        self.day = day
        time_range = os.getenv('TIME_RANGE_DAYS')
        dateobj = datetime.strptime(day, '%Y-%m-%d')
        self.range = (dateobj - timedelta(days=int(time_range))).strftime('%Y-%m-%d')
        self.config_parser = ConfigParser(config_path)

    def __get_fields_list(self) -> list:
        fields = str(os.getenv('TEMPLATE_FIELDS'))
        return fields.split(',')
    
    def get_data_file_path(self) -> str:
        filename = self.day + '-' + os.getenv('CSV_SUBDIR') + '.csv'
        path = self.file_util.get_gen_path(os.getenv('CSV_SUBDIR'))
        return path + '/' + filename

    def parse_links(self, links: dict) -> str:
        urls = []
        for key, value in links.items():
            urls.append('[' + key.capitalize() + '](' + value + ')')

        return ' '.join(urls)
    
    def parse_row_to_template(self, values: list) -> str:
        template = str(os.getenv('TEMPLATE'))
        separator = os.getenv('TEMPLATE_SEPARATOR')
        template_split = template.split(separator)
        map = dict(zip(self.fields, values))
        
        for index, part in enumerate(template_split):
            if part in map.keys():
                template_split[index] = map[part]
        
        parsed = ''.join(template_split)
        return parsed.replace('\\r\\n', '\r\n')

    def read_data_to_string(self) -> str:
        date_tag = str(os.getenv('DATE_TAG'))
        data = pd.read_csv(self.get_data_file_path(), index_col='pkey', sep=';', parse_dates=[date_tag])
        data.info()
        filter = data.loc[(data[date_tag] >= self.range)].sort_values(date_tag)

        output = ''

        for index, row in filter.iterrows():
            values = []
            feed_key = row[str(os.getenv('FEED_UID'))]
            settings = self.config_parser.get_settings_for_feed_key(feed_key)

            for field in self.fields:
                value = ''
                if row.get(field, 'NaN') != 'NaN':
                    value = row[field]
                elif settings.get(field, 'NaN') != 'NaN':
                    value = settings[field]
                    if field == str(os.getenv('LINK_TAG')):
                        value = self.parse_links(value)

                values.append(str(value))
                
            output += self.parse_row_to_template(values)
        
        return output
    
    def generate_text_file(self, format: str = 'txt') -> None:
        output = self.read_data_to_string()

        path = self.file_util.make_gen_path(str(os.getenv('OUTPUT_SUBDIR')))
        filename = self.day + '-output.' + format
        
        try:
            self.file_util.save_to_path_utf8(output, path + '/' + filename)
            self.logger.log('Output saved.')
        except Exception as err:
            self.logger.log(
                'Unable to save output to: ' + path + '/' + filename + ' ' + err, self.logger.LEVEL_ERROR)