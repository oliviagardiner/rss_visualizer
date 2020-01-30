import csv
import os
import pandas
import xml.etree.ElementTree as ET
from datetime import date
from src.rss_downloader import RssDownloader

ABS_PATH = os.path.dirname(__file__)

class RssCsvParser(RssDownloader):
    data_keys = ['key', 'guid', 'pubDate', 'title', 'description', 'category', 'link']

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_config.json', download_dirname = 'rss_downloads', abs_path = None, log_dirname = 'rss_logs', logger_name = __name__, stat_dirname = 'rss_statistics', csv_filename = 'data.csv'):
        RssDownloader.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

        self.stat_filepath = self.convert_to_abs_path(stat_dirname, is_dir = True)
        self.csv_filepath = self.convert_to_abs_path(stat_dirname + '/' + self.today + '_' + csv_filename)
    
    def parse_xml_to_dataframe(self, key):
        """Reads all the xml files generated on the specific day and parses them into a pandas dataframe object.
        
        Returns
        ---
        dataframe (object)
        """
        filelist = self.get_file_list(key)

        df = pandas.DataFrame(columns = self.data_keys)
        
        for filename in filelist:
            tree = ET.parse(filename)
            enclosing_tag = self.get_config_settings('enclosing_tag_name') if isinstance(self.get_config_settings('enclosing_tag_name'), str) else 'item'

            for node in tree.findall('.//' + enclosing_tag):
                row = {'key': key, 'guid': None, 'pubDate': '', 'title': '', 'description': '', 'category': [], 'link': ''}
                for child in node.iter():
                    if child.tag in self.data_keys:
                        value = self.clean_html(child.text) or None
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
        """Saves the pandas dataframe to a csv file.
        """
        df.index.name = 'pkey'
        df = df.drop_duplicates(subset = ['guid']) # debatable
        df.to_csv(self.csv_filepath, encoding = 'utf-8', sep = ';')

    def run(self):
        urls = self.get_config()
        df = pandas.DataFrame(columns = self.data_keys)
        for key in urls.keys():
            df_dataset = self.parse_xml_to_dataframe(key)
            df = df.append(df_dataset, ignore_index = True)
        self.save_data_to_csv(df)
        self.logger.info('CSV data parsing finished, time elapsed: %s'%(self.get_time_elapsed()))