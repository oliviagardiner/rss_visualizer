#!/usr/bin/python3

import sys
import os
# abs_path = os.path.dirname(__file__)
# sys.path.append(abs_path)

from src.rss_downloader import RssDownloader

# Schedules RSS feed downloader

dl = RssDownloader()
dl.run()
