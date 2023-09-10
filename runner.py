#!/usr/bin/python3

from src.processor import Processor
from src.csv_parser import CsvParser
from src.output_generator import OutputGenerator
from src.wordcloud_generator import WordcloudGenerator

config = 'rss_config.json'

dl = Processor(config)
dl.get_rss_for_urls()

pa = CsvParser(config, 'key')
pa.parse_sources_to_csv()

ge = OutputGenerator(config)
ge.generate_text_file()

woc = WordcloudGenerator(config)
woc.generate_wordcloud_for_tags()