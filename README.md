# RSS PARSER

## What's this?

These are simple scripts that you can add to a scheduler daemon (eg. cron) to automatically pull RSS feeds from news sites of your preference. An RSS feeds is a list of articles that are structured in a strict way, using a markup language called XML. Why are we downloading all these summaries? This repository also comes with a parser that allows you to perform simple statistical analysis on the article headlines and descriptions. This statistical analysis will allow you to compare the way these news outlets cover topics based on the frequency of the words and categories they use.

You can also compare this data to the Twitter Trends API to see the extent traditional media covers certain social media topics - and also when they don't.

## Requirements

* Python 3.* installed

These instructions assume you are using Linux.

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

## Crontab setup

In the terminal, type `crontab -e` to edit your crontab. After selecting the editor (in this case nano) add the following line:

```
0,30 * * * * python3 /home/USERNAME/path/to/file/rss_parser/downloader3.7.py

```

The 0,30 at the beginning means that your script will execute twice every hour, at 0 minutes and at 30 minutes, as long as your cron daemon is running. To tell whether the cron daemon is running, type `sudo service cron status`. Add a line ending to your crontab just to be safe. The crontab saved successfully if you exited nano with Ctrl+S Ctrl+X and you get the following message in the terminal:

`crontab: installing new crontab`

The downloader file itself needs to be executable.

`chmod +x downloader3.7.py`
