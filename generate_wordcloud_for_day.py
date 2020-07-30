#!/usr/bin/python3

import sys, getopt
import os
from datetime import date, datetime
from src.rss_wordcloud_generator import RssWordcloudGenerator

# Generating word clouds

day = date.today()

try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:", ["day="])
except getopt.GetoptError:
    print ('-d <day>')
    sys.exit(1)

for opt, arg in opts:
    if opt in ("-d", "--day"):
        day = arg

date = datetime.strptime(day, '%Y-%m-%d')
gen = RssWordcloudGenerator(today = date.strftime("%Y-%m-%d"))
gen.run()
