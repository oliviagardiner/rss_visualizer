#!/usr/bin/python3.7

import sys
import os
import time
abs_path = os.path.dirname(__file__)
sys.path.append(abs_path)

from src.rss_wordcloud_generator import RssWordcloudGenerator
from src.rss_csv_parser import RssCsvParser

# Generating word clouds

gen = RssWordcloudGenerator()
gen.run()

# Parsing the XML data into CSV

ra = RssCsvParser()
ra.run()
