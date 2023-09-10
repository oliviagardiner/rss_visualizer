#!/usr/bin/python3

from src.config_parser import ConfigParser
from src.file_util import FileUtil
from src.env_util import EnvUtil
import glob
import os
import re
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

class CsvParser():
    def __init__(self, config_path: str) -> None:
        load_dotenv()
        self.file_util = FileUtil()
        self.config_parser = ConfigParser(config_path)
        self.data_keys = EnvUtil.parse_config_to_list('PARSE_FIELDS')
        self.uid_key = str(os.getenv('FEED_UID'))
        self.sources = self.config_parser.get_values_by_key('name')
        self.date_slice_config = self.config_parser.get_values_by_key(
            'date_slice')

    def __get_file_list_for_key(self, key: str) -> list:
        pattern = '*_' + key + '_rss.xml'
        path = self.file_util.get_gen_path(os.getenv('RSS_SUBDIR'))

        return glob.glob(path + '/' + pattern)
    
    def create_row_from_key(self, key: str) -> dict:
        row = dict.fromkeys(self.data_keys)
        row[self.uid_key] = key

        return row
    
    def clean_html_from_text(self, text: str) -> str:
        cl = re.compile('<.*?>')
        cl_text = re.sub(cl, '', str(text))
        cl_text = cl_text.strip()
        cl_text = cl_text.replace('\n', '')
        cl_text = cl_text.replace('\t', '')
        return cl_text
    
    def parse_rss_string_to_date(self, text: str, key: str) -> str:
        parts = text.split(',')
        date_slice = self.date_slice_config[key] or 5
        return parts[1][:-date_slice].strip()
    
    def fill_empty_guid_with_unique_value(self, row: dict) -> dict:
        if row.get(os.getenv('DROP_DUPLICATE'), '') == '':
            row[os.getenv('DROP_DUPLICATE')
                ] = row.get(os.getenv('FILL_UNIQUE'))
            
        return row

    def parse_xml_to_dataframe_for_source(self, key: str) -> pd.DataFrame:
        enclosing_tag = os.getenv('ENCLOSING_TAG')
        files = self.__get_file_list_for_key(key)

        df = pd.DataFrame(columns = self.data_keys)

        for filename in files:
            tree = ET.parse(filename)

            for node in tree.findall('.//' + enclosing_tag):
                row = self.create_row_from_key(key)

                for child in node.iter():
                    if child.tag in self.data_keys or 'encoded' in child.tag:
                        tag = child.tag if child.tag in self.data_keys else os.getenv('MAP_ENCODED_TO')

                        value = self.clean_html_from_text(child.text) or ''
                        value = value.strip()

                        if tag == os.getenv('DATE_TAG'):
                            value = self.parse_rss_string_to_date(value, key)

                        row[tag] = value

                row = self.fill_empty_guid_with_unique_value(row)
                df_row = pd.DataFrame([row.values()], columns = self.data_keys)
                df = pd.concat([df, df_row], ignore_index=True)
        
        return df

    def parse_sources_to_csv(self) -> None:
        df = pd.DataFrame(columns = self.data_keys)

        for key in self.sources.keys():
            source_dataset = self.parse_xml_to_dataframe_for_source(key)
            df = pd.concat([df, source_dataset], ignore_index=True)

        df.index.name = 'pkey'
        if isinstance(os.getenv('DROP_DUPLICATE'), str):
            df = df.drop_duplicates(subset=[os.getenv('DROP_DUPLICATE')])
        
        path = self.file_util.make_gen_path(os.getenv('CSV_SUBDIR'))
        filename = datetime.now().strftime('%Y-%m-%d') + '-' + \
            os.getenv('CSV_SUBDIR') + '.csv'
        df.to_csv(path + '/' + filename, encoding = 'utf-8', sep = ';')
