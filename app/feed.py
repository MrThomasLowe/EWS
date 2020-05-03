import feedparser
from Flask import request
from indicoio import text_tags

feed_urls = ['https://news.yahoo.com/rss/mostviewed']

def print_feed():
    entries = feedparser.parse(feed_urls)['entries']
    titles = [entry.get('title') for entry in entries]
    title_tags = batch_text_tags(titles)
    for entry, tags in zip(entries, title_tags):
        entry['tags'] = tags
    entries = [parsed(entry) for entry in entries]
    return render_template('home.html',entries=entries)
