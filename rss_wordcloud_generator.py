
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
    colors = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'summer', 'winter', 'cool', 'copper', 'twilight', 'rainbow']

    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_feeds.json', download_dirname = 'rss_downloads', abs_path = None,log_dirname = 'rss_logs', logger_name = __name__, tag = '', wordcloud_filepath = 'daily_wordclouds', stopwords_filename = 'custom_stopwords', custom_stopwords = True, allow_duplicates = False):
        RssDownloader.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

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
        """Collects all text from a specified tag per key per day and returns it as one long string.

        Returns
        ---
        string
        """
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
        """If there is text to process, this method creates a wordcloud and saves it to a .jpg.
        """
        txt = self.get_text_by_tag(tag, key)

        if (len(txt) > 0):
            if self.custom_stopwords is True:
                stopwords = self.custom_stopwords_from_file()
            else:
                stopwords = set(STOPWORDS)
            
            pathname = os.path.join(self.wordcloud_filepath, self.today + '_' + key + '_' + tag + '.jpg')

            try:
                wordcloud = WordCloud(width = 800, height = 800,
                    max_words = 100,
                    background_color = 'white',
                    colormap = color,
                    stopwords = stopwords,
                    min_font_size = 10).generate(txt)
                wordcloud.to_file(pathname)
            except:
                pass

    def get_random_colormap_color(self):
        """Returns a random matplotlib compatible colormap string.

        Returns
        ---
        string
        """
        return random.choice(self.colors)

    def run(self):
        color = self.get_random_colormap_color()
        urls, fields = self.get_config()
        for key in urls.keys():
            if (key in fields and fields[key] != None):
                tag = fields[key].get(self.tag, self.tag)
            else:
                tag = self.tag
            self.create_wordcloud(tag, key, color)
        self.logger.info('Wordcloud generating finished for tag "%s", time elapsed: %s'%(tag, self.get_time_elapsed()))

