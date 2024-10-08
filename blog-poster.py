import feedparser
import json
import os
from mastodon import Mastodon

# constants
RSS_FEED_URL = 'your_feed_url'
POSTED_ITEMS_FILE = 'posted_items.json'
INSTANCE_URL = 'your_mastodon_url'
ACCESS_TOKEN = 'your_mastodon_access_token'

# initialize Mastodon client
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=INSTANCE_URL
)

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

# post new items to Mastodon
for item in new_items:
    custom_text = "This is a line for any custom text you want to have shared along with the blog title, link, and excerpt."
    excerpt = item.summary if 'summary' in item else 'No excerpt available'
    status_message = f"{custom_text}\n{item.title}\n{item.link}\n\n{excerpt}"
    mastodon.status_post(status=status_message)
    posted_items.append(item.id)

# update the list of posted items and save it back to the file
with open(POSTED_ITEMS_FILE, 'w') as f:
    json.dump(posted_items, f)
