import csv
import os
import pandas
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from rss_downloader import RssDownloader

ABS_PATH = os.path.dirname(__file__)

class RssCsvParser(RssDownloader):
    data_keys = ['key', 'guid', 'pubDate', 'title', 'description', 'category', 'link']

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None, stat_dirname = 'daily_statistics', csv_filename = 'data.csv'):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.today = today
        self.config_filepath = json_filename
        self.download_filepath = download_dirname
        self.init_rss_downloader_paths()

        self.stat_filepath = stat_dirname
        self.csv_filepath = 'data.csv'
        self.init_rss_analytics_paths()

    def init_rss_analytics_paths(self):
        """Changes the path of the statistics directory to absolute paths. Creates the directory if it doesn't exist.
        """
        self.stat_filepath = os.path.join(self.abs_path, self.stat_filepath)
        self.csv_filepath = os.path.join(self.stat_filepath, self.today + '_' + self.csv_filepath)
        Path(self.stat_filepath).mkdir(parents=True, exist_ok=True)
    
    def parse_xml_to_dict(self, key):
        """Reads all the xml files generated on the specific day and parses them into a pandas dataframe object.
        Returns
        ---
        dataframe (object)
        """
        filelist = self.get_file_list(key)

        df = pandas.DataFrame(columns = self.data_keys)
        
        for filename in filelist:
            tree = ET.parse(filename)

            for node in tree.findall('.//item'):
                row = {'key': key, 'guid': None, 'category': []}
                for child in node.iter():
                    if child.tag in self.data_keys:
                        value = child.text or None
                        if value != None:
                            value = value.strip()
                        if child.tag is 'category':
                            row[child.tag].append(value)
                        else:
                            row[child.tag] = value
                if row['guid'] is None:
                    row['guid'] = row['link']
                df_row = pandas.DataFrame([row.values()], columns = self.data_keys)
                df = df.append(df_row, ignore_index = True)
        
        return df

    def save_data_to_csv(self, df):
        """Saves the dataframe to a csv file.
        """
        df.index.name = 'pkey'
        df = df.drop_duplicates(subset = ['guid']) # debatable
        df.to_csv(self.csv_filepath, encoding = 'utf-8', sep = ';')

    def run(self):
        urls = self.get_config()
        df = pandas.DataFrame(columns = self.data_keys)
        for key in urls.keys():
            df_dataset = self.parse_xml_to_dict(key)
            df = df.append(df_dataset, ignore_index = True)
        self.save_data_to_csv(df)