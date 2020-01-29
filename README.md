# RSS Visualizer

## What's this?

These are simple scripts that you can add to a scheduler daemon (eg. cron) to automatically pull RSS feeds from news sites of your preference. An RSS feed is a list of articles that are structured in a specific way, using a markup language called XML. Why are we downloading all these summaries? This repository allows you to statistically analyze these feeds and also lets you create word cloud visualizations for specific days to compare the news coverage of different media outlets.

You can install this script on your own server and study the RSS feeds of your choice. Be aware that this script generates roughly 1-3Mb of data per RSS feed every day (assuming the server is running continously all day).

The following will be generated:
* XML files (the downloaded raw RSS feeds)
* CSV data files (the parsed RSS feeds)
* CSV statistics files (for caching purposes so we don't have to run the statistics on all the collected data every time we need to access it)
* Wordcloud image files (.jpg)
* log files (.txt)

## Requirements

* Python 3.* installed

These instructions assume you are using Linux. The following python modules have to be installed:

```
pip install pandas
pip install wordcloud
```

## Creating the config file

Define your RSS feeds url in a json file, and name it `rss_config.json`. You can do this easily by editing the `rss_config_sample.json` and renaming it.

```
{
    "feeds": {
        "UID": {
            "url": "https://sample.com/feed",
            "name": "NAME",
            "fields": {
                "title": "TITLE",
                "category": "CATEGORY",
                "description": "DESCRIPTION"
            }
        }
    }
}
```

It's mandatory to define the `UID` and the url value for the config to work. All other attributes are optional.

The `UID` has to be a unique key as it will be also used to generate the file names for the downloaded RSS feeds. The `fields` define the name of the XML tags used for the following elements: title, category, description. There is a high chance that they will be called "title", "category" and "description" by default, but you should check a manually downloaded sample XML to see what tags are nested under `rss / channel / item`. If you don't define any of the fields, the values will default to their own keys. Just like if you don't define the `name` attribute, it will default to the UID. For example:

```
{
    "feeds": {
        "new_york_times_top_stories": {
            "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
        }
    }
}
```

## Eliminate words

If your RSS feeds are **not in English**, you can define your own list of stopwords to eliminate certain words from the final processing. Use the *custom_stopwords* file for this purpose. It doesn't need to have a file extension, and it's important that each line represents a unique word or expression. Stopwords are case insensitive.

## Crontab setup

In the terminal, type `crontab -e` to edit your crontab. After selecting the editor (in this case nano) add the following line:

```
0 * * * * python3 /home/USER/path/to/file/rss_parser/sched_downloader.py
30 * * * * python3 /home/USER/path/to/file/rss_parser/sched_analytics.py

```

The 0 at the beginning means that your script will execute once every hour as long as your cron daemon is running. To tell whether the cron daemon is running, type `sudo service cron status`. Add a line ending to your crontab just to be safe. The crontab saved successfully if you exited nano with Ctrl+S Ctrl+X and you get the following message in the terminal:

`crontab: installing new crontab`

The files need to be executable. You don't need to use `python3` in the command (`python` is enough) in case there is only one version of python installed on your server, or python3 is set as default.

## Issues

This analysis currently does not aggregate words that share the same oblique stem, therefore it works less well for languages that use suffixation.
