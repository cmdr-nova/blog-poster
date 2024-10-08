import feedparser
import json
import os
import requests
from mastodon import Mastodon

# constants
RSS_FEED_URL = 'your_blog_rss_feed'
POSTED_ITEMS_FILE = 'posted_items.json'
INSTANCE_URL = 'your_mastodon_instance_url'
ACCESS_TOKEN = 'your_mastodon_access_token'
DISCORD_WEBHOOK_URL = 'your_discord_webhook'

# initialize Mastodon client
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=INSTANCE_URL
)

def share_to_discord(title, link, excerpt):
    data = {
        'content': f"{title}\n{link}\n\n{excerpt}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()

# load the list of already posted items
if os.path.exists(POSTED_ITEMS_FILE):
    with open(POSTED_ITEMS_FILE, 'r') as f:
        posted_items = json.load(f)
else:
    # initialize the list with current RSS items
    feed = feedparser.parse(RSS_FEED_URL)
    posted_items = [entry.id for entry in feed.entries]
    # save the initial list to the file
    with open(POSTED_ITEMS_FILE, 'w') as f:
        json.dump(posted_items, f)

# fetch the RSS feed and parse it
feed = feedparser.parse(RSS_FEED_URL)

# check for new items in the RSS feed
new_items = [entry for entry in feed.entries if entry.id not in posted_items]

# post new items to Mastodon and Discord
for item in new_items:
    custom_text = "Put your own text in here that shares with each blog post!"
    excerpt = item.summary if 'summary' in item else 'No excerpt available'
    status_message = f"{custom_text}\n{item.title}\n{item.link}\n\n{excerpt}"
    
    # post to Mastodon
    mastodon.status_post(status=status_message)
    
    # post to Discord
    share_to_discord(item.title, item.link, excerpt)
    
    # add item ID to posted items
    posted_items.append(item.id)

# update the list of posted items and save it back to the file
with open(POSTED_ITEMS_FILE, 'w') as f:
    json.dump(posted_items, f)
