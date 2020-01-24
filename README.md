# Requirements

* Python 3 installed

These instructions assume you are using Linux.

# Creating the source file

Define your key-value pairs of a name and an RSS feed url in a json, and name it `rss_feeds.json`

```
{
    "feeds": {
        "key": "https://sample.com/feed"
    }
}
```

# Crontab setup

In the terminal, type `crontab -e` to edit your crontab. After selecting the editor (in this case nano) add the following line:

```
#Borrowed from anacron
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#End borrowed from anacron

0,30 * * * * python3 /home/USERNAME/path/to/file/rss_parser/downloader3.7.py

```

The 0,30 at the beginning means that your script will execute twice every hour, at 0 minutes and at 30 minutes, as long as your cron daemon is running. To tell whether the cron daemon is running, type `sudo service cron status`. Add a line ending to your crontab just to be safe. The crontab saved successfully if you exited nano with Ctrl+S Ctrl+X and you get the following message in the terminal:

`crontab: installing new crontab`

The downloader file itself needs to be executable.

`chmod +x downloader3.7.py`
