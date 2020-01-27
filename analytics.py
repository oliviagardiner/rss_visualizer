#!/usr/bin/python3.7

import sys
import os
abs_path = os.path.dirname(__file__)
sys.path.append(abs_path)

import rss_wordcloud_generator as wcgen

wcgen.generateDailyWordclouds('title')
wcgen.generateDailyWordclouds('description')
wcgen.generateDailyWordclouds('category', allow_duplicates = True)
