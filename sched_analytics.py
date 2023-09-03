#!/usr/bin/python3

import sys
import os
from datetime import date, timedelta
# abs_path = os.path.dirname(__file__)
# sys.path.append(abs_path)

from src.rss_processor import RssProcessor
from src.rss_csv_parser import RssCsvParser
from src.rss_analytics import RssAnalytics

yesterday = date.today() - timedelta(days = 1)
yesterday = yesterday.strftime('%Y-%m-%d')

# Parsing the XML data into CSV

ra = RssCsvParser()
ra.run()

# Generate digest

an = RssAnalytics()
an.run()

# Attempting to archive yesterday's raw XMLs

arch = RssProcessor()
arch.archive_day(yesterday)
