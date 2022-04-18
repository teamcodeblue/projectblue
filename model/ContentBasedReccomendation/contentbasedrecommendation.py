import torch
from transformers import BertTokenizer
from torch import nn
from model_defs import ArticleClassifier
import pymongo
import json

class FeatureExtractor():
    def __init__(self, path, device='cpu'):
        self.model = torch.load(path, map_location=torch.device(device))
        self.model.eval()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

    def extract_features(self, text):
        text = str(text)
        embeded = self.tokenizer(text, padding='max_length', max_length = 512, truncation=True, return_tensors="pt")
        output = self.model(embeded['input_ids'], embeded['attention_mask'])
        return output
    def categorize(self, text):
        return torch.argmax(self.extract_features(text), dim=1)
class SimpleContentBasedRecommender(FeatureExtractor):
    def __init__(self, path, device='cpu'):
        super(SimpleContentBasedRecommender, self).__init__(path, device='cpu')
        self.interacted = torch.zeros(1,5)
        self.interacted_count = 0

        
    def addInteracted(self, text):
        features = self.extract_features(text)
        self.interacted += features
        self.interacted_count += 1

    def reccommend(self, data, target=None):
        if target is None:
            target = self.interacted / self.interacted_count
        features = self.extract_features(data)
        scores = torch.matmul(target, features.T)
        return scores



def reccomendations():
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

    client = pymongo.MongoClient(
        "mongodb://127.0.0.1:27017/")
    db = client["test_database"]
    collection = db["test_collection"]
    #collection.delete_many({})

    #collection.insert_one({"url": "bbc.html", "html": str(open("../RSSfuncs/scottsdummydb/bbc.html").read())})

    query   = collection.find_one({"url":"bbc.html"})["html"]
    #print(query)

    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import os
    html = query
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)
    #


    FE = SimpleContentBasedRecommender("model.pt")
    FE.addInteracted(text)
    for feed in feeds:
        NewsFeed = feedparser.parse(feed)
        val = 0
        minima  = 1000
        for entry in NewsFeed.entries:
            #print(entry["title_detail"])
            val = FE.reccommend(entry["title_detail"]["value"]).detach().numpy()[0][0]
            if  val < minima:
                print(val, entry["title_detail"]["value"])
                minima = val
    return ""

reccomendations()