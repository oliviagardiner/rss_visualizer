#!/usr/bin/python3

from src.file_logger import FileLogger
from src.config_parser import ConfigParser
from src.file_util import FileUtil
from src.env_util import EnvUtil
from src.output_generator import OutputGenerator
from dotenv import load_dotenv
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
import pandas as pd
import os
import random

class WordcloudGenerator():
    def __init__(self, config_path: str) -> None:
        load_dotenv()
        self.config_parser = ConfigParser(config_path)
        self.file_util = FileUtil()
        self.logger = FileLogger('default')
        self.output_generator = OutputGenerator(config_path)
        self.colormaps = EnvUtil.parse_config_to_list('COLORMAPS')
        self.cloud_fields = EnvUtil.parse_config_to_list('CLOUD_FIELDS')
        self.custom_stopwords = EnvUtil.parse_config_to_list('STOPWORDS') or None
        self.wordcloud_subdir = os.getenv('WORDCLOUD_SUBDIR')
    
    def create_wordcloud_from_text(self, txt: str, color: str, postfix: str = ''):
        subdir_name = str(os.getenv('WORDCLOUD_SUBDIR'))

        if (len(txt) > 0):
            stopwords = self.custom_stopwords if self.custom_stopwords != None else set(STOPWORDS)

            imagepath = self.file_util.make_gen_path(
                subdir_name) + '/' + datetime.now().strftime('%Y-%m-%d') + '-' + subdir_name + '_' + postfix + '.png'
            
            try:
                wordcloud = WordCloud(width=int(os.getenv('WOC_WIDTH')) or 800,
                                      height=int(os.getenv('WOC_HEIGHT')) or 800,
                                      max_words=int(os.getenv('WOC_MAX_WORDS')) or 100,
                                      background_color=str(os.getenv('WOC_BACKGROUND_COLOR')) or 'white',
                                      colormap=color,
                                      stopwords=stopwords,
                                      min_font_size=10).generate(txt)
                wordcloud.to_file(imagepath)
            except Exception as err:
                self.logger.log(
                    'Could not generate worldcloud at path: %s' % (imagepath) + ' ' + str(err), self.logger.LEVEL_ERROR)
                
    def get_text_from_source(self, key: str, field: str, allow_duplicates: bool = False):
        txt = [] if allow_duplicates == True else set()

        date_tag = str(os.getenv('DATE_TAG'))
        data = pd.read_csv(self.output_generator.get_data_file_path(),
                           index_col='pkey', sep=';', parse_dates=[date_tag])
        filter = data[data['key'].str.contains(key, case=False)]

        for index, row in filter.iterrows():
            if row.get(field, 'NaN') != 'NaN':
                value = str(row[field])
                txt.append(value) if allow_duplicates == True else txt.add(
                    value)

        return ' '.join(txt)

    
    def generate_wordcloud_for_tags(self) -> None:
        urls = self.config_parser.get_values_by_key('url')

        for field in self.cloud_fields:
            color = random.choice(self.colormaps)
            for key in urls.keys():
                txt = self.get_text_from_source(key, field)
                self.create_wordcloud_from_text(txt, color, key + '_' + field)
            self.logger.log('Wordcloud generating finished for field : ' + field)

