# RSS word cloud parser

## What's this?

These are simple scripts that you can add to a scheduler daemon (eg. cron) to automatically pull RSS feeds from news sites of your preference. An RSS feed is a list of articles that are structured in a specific way, using a markup language called XML. Why are we downloading all these summaries? This repository allows you to statistically analyze these feeds and also lets you create word cloud visualizations for specific days to compare the news coverage of different media outlets.

Plan: compare these to Twitter Trends API.

## Requirements

* Python 3.* installed

These instructions assume you are using Linux. The following python modules have to be installed:

```
pip install matplotlib
pip install pandas
pip install wordcloud
```

## Creating the source file

Define your RSS feeds url in a json file, and name it `rss_feeds.json`

```
{
    "feeds": {
        "UNIQUE_NAME": {
            "domain": "https://sample.com/feed",
            "fields": {
                "title": "TITLE",
                "category": "CATEGORY",
                "description": "DESCRIPTION"
            }
        }
    }
}
```

The `UNIQUE_NAME` has to be a unique key as it will be also used to generate the file names for the downloaded RSS feeds. Everything that is defined with capital letters only, must be set for each feed, by you (as well as the domain url). The `fields` define the name of the XML tags used for the following elements: title, category, description. There is a high chance that they will be called "title", "category" and "description" by default, but you should check a manually downloaded sample XML to see what tags are nested under `rss / channel / item`. If you don't define any of the fields, the values will default to their own keys. For example:

```
{
    "feeds": {
        "new_york_times_top_stories": {
            "domain": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
        }
    }
}
```

## Eliminate words

If your RSS feeds are **not in English**, you can define your own list of stopwords to eliminate certain words from the final processing. Use the *custom_stopwords* file for this purpose. It doesn't need to have a file extension, and it's important that each line represents a unique word or expression.

## Crontab setup

In the terminal, type `crontab -e` to edit your crontab. After selecting the editor (in this case nano) add the following line:

```
0 * * * * python3 /home/USERNAME/path/to/file/rss_parser/downloader3.7.py
30 * * * * python3 /home/USERNAME/path/to/file/rss_parser/rss_wordcloud_generator.py

```

The 0 at the beginning means that your script will execute once every hour as long as your cron daemon is running. To tell whether the cron daemon is running, type `sudo service cron status`. Add a line ending to your crontab just to be safe. The crontab saved successfully if you exited nano with Ctrl+S Ctrl+X and you get the following message in the terminal:

`crontab: installing new crontab`

The files need to be executable.

`chmod +x downloader3.7.py`
