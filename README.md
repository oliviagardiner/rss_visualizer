# RSS Visualizer

## What's this?

These are simple scripts that you can add to a scheduler daemon (eg. cron) to automatically pull RSS feeds from news sites of your preference. An RSS feed is a list of articles that are structured in a specific way, using a markup language called XML. Why are we downloading all these summaries? This repository allows you to statistically analyze these feeds and also lets you create word cloud visualizations for specific days to compare the news coverage of different media outlets.

<p align="center">
    <img src="https://github.com/oliviaisarobot/rss_visualizer/blob/master/preview/2020-05-18_hvg_title.png" width="300" height="300"> <img src="https://github.com/oliviaisarobot/rss_visualizer/blob/master/preview/2020-05-18_index_title.png" width="300" height="300"> <img src="https://github.com/oliviaisarobot/rss_visualizer/blob/master/preview/2020-05-18_origo_title.png" width="300" height="300"> <img src="https://github.com/oliviaisarobot/rss_visualizer/blob/master/preview/2020-05-18_pesti_sracok_title.png" width="300" height="300">
</p>

The above images are wordclouds generated for 4 Hungarian news sites based on their RSS feeds of 2020-05-18, using article titles (hvg.hu, index.hu, origo.hu, pesti_sracok.hu)

You can install this script on your own server and study the RSS feeds of your choice. Be aware that this script generates roughly 1-3Mb of data per RSS feed every day (assuming the server is running continously all day).

The following will be generated:
* XML files (the downloaded raw RSS feeds)
* CSV data files (the parsed RSS feeds)
* Wordcloud image files (.png)
* log files

## Requirements

* Python 3.* installed

These instructions assume you are using Linux. The following python modules have to be installed:

```
python -m pip install -r requirements.txt 
```

Run tests:

```
python -m unittest discover
```

Or simply:

```
docker compose up -d
```

## Creating the config file

Define your RSS feeds url in a json file, and name it `rss_config.json`. You can do this easily by editing the `rss_config_sample.json` and renaming it.

```
{
    "feeds": {
        "UID": {
            "url": "https://sample.com/feed",
            "name": "NAME",
            "date_slice": 4
        }
    }
}
```

It's mandatory to define the `UID` and the `url` value for the config to work. All other attributes are optional.

The `UID` has to be a unique key as it will be also used to generate the file names for the downloaded RSS feeds.

The `date_slice` is an adjustment field to help parse the dates extracted from the XML to be compatibe with pandas DataFrame date types.

```
{
    "feeds": {
        "new_york_times_top_stories": {
            "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
            "date_slice": 4
        }
    }
}
```

### Additional settings

The environment variables allow you control a great deal of settings, including simple output templates, directory and file names and more.

## Eliminate words

If your RSS feeds are **not in English**, you can define your own list of stopwords to eliminate certain words from the final processing. Use the *custom_stopwords* file for this purpose. It doesn't need to have a file extension, and it's important that each line represents a unique word or expression. Stopwords are case insensitive.

## Known issues

This analysis currently does not aggregate words that share the same oblique stem, therefore it works less well for languages that use suffixation.
