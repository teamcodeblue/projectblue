import torch
from transformers import BertTokenizer
from torch import nn
from model.ContentBasedReccomendation.model_defs import ArticleClassifier
import pymongo
import json
import queue
Cache_result = None

class FeatureExtractor():
    def __init__(self, path, device='cpu'):
        self.model = torch.load(path, map_location=torch.device(device))
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
        self.interacted = torch.zeros(1,5).to("cpu")
        self.interacted_count = 0

        
    def addInteracted(self, text):
        #self.model = self.model.to('cuda:0')
        features = self.extract_features(text)
        self.interacted += features
        self.interacted_count += 1

    def reccommend(self, data, target=None):
        if target is None:
            target = self.interacted / self.interacted_count
        features = self.extract_features(data)
        scores = torch.matmul(target, features.T) / (target.norm() * features.T.norm())
        return scores


def reccomendations(model_link = "model.pt", Globals=None):
    import feedparser

    val1 = 1
    val2 = 15
    val3 = 45
    feeds = ["https://www.reddit.com/r/tech.rss, https://www.reddit.com/r/fishing.rss"]

    client = pymongo.MongoClient(
        "mongodb://127.0.0.1:27017/")
    db = client["test_database"]
    collection = db["test_collection"]
    #collection.delete_many({})

    #collection.insert_one({"url": "bbc.html", "html": str(open("../RSSfuncs/scottsdummydb/bbc.html").read())})
    N = 2
    querys = collection.find().skip(max(0,collection.count_documents({}, skip = 0) - N))
    from bs4 import BeautifulSoup

    for n in range(N):
        Globals.PROGRESS = ((n+1)/N)*100
        try:
            query   = querys[n]
            #print(query)
        except IndexError:
            break

        from urllib.request import urlopen
        import os
        html = str(query)

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

        #print(text)
        #


        FE = SimpleContentBasedRecommender("model/ContentBasedReccomendation/model.pt")
        FE.addInteracted(text)
        print("done")

    que = []
    minima = 1000
    Globals.PROGRESS = 0
    iter = 0
    for feed in feeds:
        iter += 1
        Globals.PROGRESS = float(iter / len(feeds))*100
        print(float(iter / len(feeds)))
        NewsFeed = feedparser.parse(feed)

        val = 0

        for entry in NewsFeed.entries:


            #print(entry["title_detail"])
            val = FE.reccommend(entry["title_detail"]["value"]).cpu().detach().numpy()[0][0]
            if  val < minima:
                if "content" in entry:
                    for c in entry["content"]:
                        if "link" in str(c):
                            que.append(str(entry["title_detail"]["value"]) + str(c['value']) + "\n")


                else:
                    que.append(str(entry["title_detail"]["value"]) + str(entry["title_detail"]["base"]) + "\n")

                print(val, (entry["title_detail"]["value"]))
                minima = val

    print(que)
    Cache_result = que[max(0,len(que)-5):]
    return que[max(0,len(que)-5):]

