#!/usr/bin/python3.7

import urllib.request
from urllib.error import HTTPError
from datetime import datetime
from pathlib import Path
import json
import os

abs_path = os.path.dirname(__file__)

json_filename = os.path.join(abs_path, 'rss_feeds.json')
gen_path = os.path.join(abs_path, 'rss_downloads')

Path(gen_path).mkdir(parents=True, exist_ok=True)

def convertJsonToDict():
    global json_filename
    urls = dict()
    with open(json_filename) as json_file:
        data = json.load(json_file)
        for key in data['feeds']:
            urls[key] = data['feeds'].get(key, '').get('domain', '')
    return urls

def getDateFormatted():
    now = datetime.now()
    return now.strftime('%Y-%m-%d-%H%M%S')

def getFilePath(key):
    global gen_path
    return gen_path + '/' + getDateFormatted() + '_' + key + '_rss.xml'

def logError(err, url):
    global gen_path
    msg =  getDateFormatted() + ' Error trying to download file from url: [' + url + '] ' + str(err.code) + ': ' + str(err.reason)
    f = open(gen_path + '/log.txt', 'a+')
    f.write(msg + '\n')
    f.close()

# Some servers will reject your request if the User-Agent header is not set
# so we make a 2nd attempt if the first try throws a 403 (Forbidden) error code

def downloadUrls(d =dict()):
    for key, val in d.items():
        try:
            urllib.request.urlretrieve(val, getFilePath(key))
        except HTTPError as err:
            if err.code == 403:
                try:
                    opener = urllib.request.URLopener()
                    opener.addheader('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0')
                    opener.retrieve(val, getFilePath(key))
                except HTTPError as err:
                    logError(err, val)
            else:   
                logError(err, val)

urls = convertJsonToDict()
downloadUrls(urls)
