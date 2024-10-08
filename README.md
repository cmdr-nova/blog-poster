Hello! This is my third little bot. This guy will go onto your VPS and live in 5 minute intervals. But let me explain. I got tired of the slog of having to copy and paste the links from my new posts, and then having to type up something about them, and then also hit the post button. So I made this bot to do it for me, instead.

What it does:

- Upon initial load, it will check your feed for all existing links, and parse them into a brand new json file, automatically. It does this, so that when it runs the rest of the script, it doesn't spam your entire Mastodon feed with a billion posts and links, and from this point forward, will *only* look for brand new feed items.
- Once a new blog post emerges into your RSS feed, it posts to Mastodon, and then adds that brand new item to the aforementioned json, that acts as an effective ignore list.

*The reason I set it up like this, is because Jekyll sometimes does this weird thing where, if you just grab from the RSS feed all willy nilly without ignoring old entries, it'll re-share those old entries at random whenever you build the site. You know. When you're updating it ... But not anymore!*

That's it!

Do this:

```
pip install feedparser Mastodon.py
```

Then, use Nano to create the path and also the file.

```
nano path/you/want/blog-poster.py
```

Paste the source code into it, then edit the credentials to match what you're using. For Mastodon API, go into the Developer tab under preferences, create an app, and grab the access key. For the RSS feed, that's pretty self explanatory.

Once complete, write out, then exit Nano.

Set us up the job!

Make sure the script is executable ...

```
chmod +x /path/to/blog-poster.py
```

Open up the cron ...

```
crontab -e
```

Set it to check every five minutes for new posts (you can set the timer to be longer, I just prefer to have it check all the time, and fast).

```
*/5 * * * * /usr/bin/python3 /path/to/blog-poster.py
```

Done!
