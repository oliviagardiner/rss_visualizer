
import os
import random
from datetime import date
from wordcloud import WordCloud, STOPWORDS 
from src.rss_processor import RssProcessor

ABS_PATH = os.path.dirname(__file__)

class RssWordcloudGenerator(RssProcessor):
    def __init__(self, today = date.today().strftime('%Y-%m-%d'), json_filename = 'rss_config.json', download_dirname = 'rss_downloads', abs_path = None,log_dirname = 'rss_logs', logger_name = __name__, wordcloud_filepath = 'rss_wordclouds', stopwords_filename = 'custom_stopwords', custom_stopwords = True, allow_duplicates = False):
        RssProcessor.__init__(self, today = today, json_filename = json_filename, download_dirname = download_dirname, abs_path = abs_path, log_dirname = log_dirname, logger_name = logger_name)

        self.colors = self.get_config_settings('colormaps') if isinstance(self.get_config_settings('colormaps'), list) else ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'summer', 'winter', 'cool', 'copper', 'twilight', 'rainbow']
        self.tags = self.get_config_settings('tags') if isinstance(self.get_config_settings('tags'), list) else ['title', 'description', 'category']
        self.allow_duplicates = allow_duplicates
        self.custom_stopwords = custom_stopwords
        self.wordcloud_filepath = self.convert_to_abs_path(wordcloud_filepath + '/' + self.today, is_dir = True)
        self.stopwords_filepath = os.path.join(self.abs_path, stopwords_filename)

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
        txt = self.get_text_by_tag(tag, key, allow_duplicates = self.allow_duplicates)

        if (len(txt) > 0):
            if self.custom_stopwords is True:
                stopwords = self.custom_stopwords_from_file()
            else:
                stopwords = set(STOPWORDS)
            
            pathname = os.path.abspath(os.path.join(self.wordcloud_filepath, self.today + '_' + key + '_' + tag + '.jpg'))

            try:
                wordcloud = WordCloud(width = 800, height = 800,
                    max_words = 100,
                    background_color = 'white',
                    colormap = color,
                    stopwords = stopwords,
                    min_font_size = 10).generate(txt)
                wordcloud.to_file(pathname)
            except:
                self.logger.warning('Could not generate worldcloud at path: %s'%(pathname))

    def get_random_colormap_color(self):
        """Returns a random matplotlib compatible colormap string.

        Returns
        ---
        string
        """
        return random.choice(self.colors)

    def run(self):
        for tag in self.tags:
            color = self.get_random_colormap_color()
            urls, fields = self.get_config(urls_only = False)
            for key in urls.keys():
                if (key in fields and fields[key] != None):
                    tag = fields[key].get(tag, tag)
                self.create_wordcloud(tag, key, color)
            self.logger.info('Wordcloud generating finished for tag "%s", time elapsed: %s'%(tag, self.get_time_elapsed()))
        self.logger.info('Module finished, time elapsed: %s'%(self.get_time_elapsed()))

