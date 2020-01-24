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

Python 3 is required to execute the script!

`crontab -e`

After selecting the editor (preferably nano) add the following line:

```
#Borrowed from anacron
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#End borrowed from anacron

5 * * * * python3 /home/USERNAME/path/to/file/rss_parser/downloader3.7.py

```

The 5 at the beginning means that your script will execute 5 minutes after every hour, as long as your cron daemon is running. Add a line ending to your crontab just to be safe. The crontab saved successfully if you exited nano with Ctrl+S Ctrl+X and you get the following message in the terminal:

`crontab: installing new crontab`

The file itself needs to be executable.

```
-rwxrwxr-x 1 user user  795 jan   24 03:08 downloader.py
```
