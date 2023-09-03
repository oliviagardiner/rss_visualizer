#!/bin/bash

echo -e 'Downloading RSS feeds...'
python sched_downloader.py
echo -e 'Downloading finished.'

echo -e 'Generating digest...'
python sched_analytics.py
echo -e 'Digest generated.'