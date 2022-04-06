import feedparser
val1 = 1
val2 = 15
val3 = 45
feeds = ["https://www.reddit.com/r/tech.rss",
         "https://www.reddit.com/r/SkincareAddiction.rss",
         "https://www.reddit.com/r/Fishing.rss",
         "http://rss.cnn.com/rss/cnn_topstories.rss",
         "https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml",
         "https://www.huffpost.com/section/front-page/feed?x=1",
         "http://feeds.foxnews.com/foxnews/latest",
         "http://rssfeeds.usatoday.com/UsatodaycomNation-TopStories",
         "https://feeds.npr.org/1001/rss.xml",
         "https://www.politico.com/rss/politicopicks.xml",
         "https://www.yahoo.com/news/rss",
         "https://www.latimes.com/local/rss2.0.xml",
         "http://feeds.feedburner.com/breitbart"]
dirty_train = {"bbc.html" : val1, "nvidia.html":val2,"reddit.html":val3}

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

html = open("scottsdummydb/bbc.html")
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)


for feed in feeds:
    NewsFeed = feedparser.parse(feed)
    for entry in NewsFeed.entries:
        print(entry["title_detail"])





