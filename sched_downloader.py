#!/usr/bin/python3.7

import sys
import os
abs_path = os.path.dirname(__file__)
sys.path.append(abs_path)

from rss_downloader import RssDownloader

dl = RssDownloader()
dl.run()