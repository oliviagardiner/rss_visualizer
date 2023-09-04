#!/usr/bin/python3

from src.processor import Processor
from src.csv_parser import CsvParser
from src.output_generator import OutputGenerator

dl = Processor('rss_config.json')
dl.get_rss_for_urls()

pa = CsvParser('rss_config.json', ['key', 'guid',
               'pubDate', 'title', 'description'], 'key')
pa.parse_sources_to_csv()

ge = OutputGenerator('rss_config.json')
ge.generate_text_file()
