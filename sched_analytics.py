#!/usr/bin/python3.7

import sys
import os
from datetime import date, timedelta
abs_path = os.path.dirname(__file__)
sys.path.append(abs_path)

from src.rss_processor import RssProcessor
from src.rss_wordcloud_generator import RssWordcloudGenerator
from src.rss_csv_parser import RssCsvParser

yesterday = date.today() - timedelta(days = 1)
yesterday = yesterday.strftime('%Y-%m-%d')

# Attempting to archive yesterday's raw XMLs

arch = RssProcessor()
arch.archive_day(yesterday)

# Generating word clouds

gen = RssWordcloudGenerator()
gen.run()

# Parsing the XML data into CSV

ra = RssCsvParser()
ra.run()
