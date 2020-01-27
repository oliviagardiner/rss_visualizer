# import pandas as pd 
import os
import json
import glob
from datetime import date, timedelta
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS 
from xml.dom import minidom
from xml.dom.minidom import Node

custom_stopwords_filename = 'custom_stopwords'

abs_path = os.path.dirname(__file__)
gen_path = os.path.join(abs_path, 'rss_downloads')
wordc_path = os.path.join(abs_path, 'daily_wordclouds')
json_filename = os.path.join(abs_path, 'rss_feeds.json')

Path(wordc_path).mkdir(parents=True, exist_ok=True)

def convertJsonToDict():
    global json_filename

    urls = dict()
    fields = dict()
    with open(json_filename) as json_file:
        data = json.load(json_file)
        for key in data['feeds']:
            urls[key] = data['feeds'].get(key, '').get('domain', '')
            fields[key] = data['feeds'].get(key, '').get('fields', None)

    return urls, fields

def getTextByTag(tag, key, day = None):
    filelist = getFilelist(key, day)
    text = []

    for filename in filelist:
        doc = minidom.parse(filename)
        items = doc.getElementsByTagName('item')

        for elem in items:
            for child in elem.childNodes:
                if (child.nodeType == Node.ELEMENT_NODE and child.tagName == tag):
                    text.append(child.firstChild.data)

    return ' '.join(text)

def getFilelist(key, day = None):
    global gen_path

    if (day != None):
        pattern = day + '-*_' + key + '_rss.xml'
    else:
        pattern = '*_' + key + '_rss.xml'
    pattern = os.path.join(gen_path, pattern)

    return glob.glob(pattern)

def customStopwordsFromFile():
    global abs_path, custom_stopwords_filename

    stopwords_path = os.path.join(abs_path, custom_stopwords_filename)
    sw_file = open(stopwords_path, 'r+', encoding='utf-8')
    lines = sw_file.readlines()
    sw_file.close()

    sw_list = []

    for line in lines:
        line = line.replace('\n', '')
        sw_list.append(line)

    return set(sw_list)

def createWordcloud(tag, key, day = None, custom_stopwords = False, color = 'cividis', bg = '#1b1b1b'):
    global wordc_path

    if (day == None):
        now = date.today()
        day = now.strftime('%Y-%m-%d')

    txt = getTextByTag(tag, key, day)

    if (len(txt) > 0):
        if (custom_stopwords == True):
            stopwords = customStopwordsFromFile()
        else:
            stopwords = set(STOPWORDS)
        
        pathname = os.path.join(wordc_path, day + '_' + key + '_' + tag + '.jpg')

        wordcloud = WordCloud(width = 800, height = 800,
            max_words = 100,
            background_color = bg,
            colormap = color,
            stopwords = stopwords,
            min_font_size = 10).generate(txt)
        wordcloud.to_file(pathname)

def generateDailyWordclouds(tag):
    urls, fields = convertJsonToDict()
    today = date.today()
    # yesterday = today - timedelta(days=1)
    for key in urls.keys():
        if (key in fields and fields[key] != None):
            tag = fields[key].get(tag, tag)
        createWordcloud(tag, key, day = today.strftime('%Y-%m-%d'), custom_stopwords = True, color ='plasma', bg = 'white')

generateDailyWordclouds('title')