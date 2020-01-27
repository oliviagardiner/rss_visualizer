import sys
import os
import json
import random
from datetime import date
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS 
from xml.dom import minidom
from xml.dom.minidom import Node
from rss_downloader import RssDownloader

ABS_PATH = os.path.dirname(__file__)

class RssWordcloudGenerator(RssDownloader):

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None, tag = '', wordcloud_filepath = 'daily_wordclouds', stopwords_filename = 'custom_stopwords', custom_stopwords = True, allow_duplicates = False):
        if abs_path is None:
            abs_path = ABS_PATH
        self.abs_path = abs_path
        self.today = today
        self.config_filepath = json_filename
        self.download_filepath = download_dirname
        self.init_rss_downloader_paths()

        self.tag = tag
        self.allow_duplicates = allow_duplicates
        self.custom_stopwords = custom_stopwords
        self.stopwords_filepath = stopwords_filename
        self.wordcloud_filepath = wordcloud_filepath
        self.init_rss_wordcloud_generator_paths()

    def init_rss_wordcloud_generator_paths(self):
        """Changes the path of the wordcloud directory to absolute paths. Creates the directory if it doesn't exist.
        """
        self.wordcloud_filepath = os.path.join(self.abs_path, self.wordcloud_filepath + '/' + self.today)
        self.stopwords_filepath = os.path.join(self.abs_path, self.stopwords_filepath)
        Path(self.wordcloud_filepath).mkdir(parents=True, exist_ok=True)

    def get_config(self):
        """Creates a uid-url dictionary and a uid-fields dictionary from the json config.
        Returns
        ---
        lists (urls, fields)
        """
        urls = dict()
        fields = dict()
        with open(self.config_filepath) as json_file:
            data = json.load(json_file)
            for key in data['feeds']:
                urls[key] = data['feeds'].get(key, '').get('domain', '')
                fields[key] = data['feeds'].get(key, '').get('fields', None)

        return urls, fields

    def get_text_by_tag(self, tag, key):
        if self.allow_duplicates is True:
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
                        if self.allow_duplicates is True:
                            text.append(child.firstChild.data.strip())
                        else:
                            text.add(child.firstChild.data.strip())

        return ' '.join(text)

    def custom_stopwords_from_file(self):
        """Creates a list of unique words that will be omitted from the analysis.
        Returns
        ---
        set
        """
        sw_file = open(self.stopwords_filepath, 'r+', encoding='utf-8')
        lines = sw_file.readlines()
        sw_file.close()

        sw_list = []

        for line in lines:
            line = line.replace('\n', '')
            sw_list.append(line)

        return set(sw_list)

    def create_wordcloud(self, tag, key, color = 'inferno'):
        txt = self.get_text_by_tag(tag, key)

        if (len(txt) > 0):
            if self.custom_stopwords is True:
                stopwords = self.custom_stopwords_from_file()
            else:
                stopwords = set(STOPWORDS)
            
            pathname = os.path.join(self.wordcloud_filepath, self.today + '_' + key + '_' + tag + '.jpg')

            wordcloud = WordCloud(width = 800, height = 800,
                max_words = 100,
                background_color = 'white',
                colormap = color,
                stopwords = stopwords,
                min_font_size = 10).generate(txt)
            wordcloud.to_file(pathname)

    def get_random_colormap_color(self):
        """Returns a random matplotlib compatible colormap string.
        Returns
        ---
        string
        """
        colors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper']
        return random.choice(colors)

    def run(self):
        color = self.get_random_colormap_color()
        urls, fields = self.get_config()
        for key in urls.keys():
            if (key in fields and fields[key] != None):
                tag = fields[key].get(self.tag, self.tag)
            else:
                tag = self.tag
            self.create_wordcloud(tag, key, color)

