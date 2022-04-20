import torch
from transformers import BertTokenizer
from torch import nn
from model_defs import ArticleClassifier
import numpy as np

class FeatureExtractor():
    def __init__(self, path, device='cpu'):
        self.model = torch.load(path, map_location=torch.device(device))
        self.model.eval()
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

    def extract_features(self, text):
        embeded = self.tokenizer(text, padding='max_length', max_length = 512, truncation=True, return_tensors="pt")
        output = self.model(embeded['input_ids'], embeded['attention_mask'])
        return output
    def categorize(self, text):
        return torch.argmax(self.extract_features(text), dim=1)
class SimpleContentBasedRecommender(FeatureExtractor):
    def __init__(self, path, texts , weights, device='cpu'):
        super(SimpleContentBasedRecommender, self).__init__(path, device='cpu')
        self.target = self.set_target(texts, weights)

        
    def set_target(self, texts , weights):
        self.features = self.extract_features(text).numpy()
        #normalize
        self.features /= np.sum(self.features, dim=1)
        self.weights = weights
    def append(self, texts, weights):
        toAdd = self.extract_features(text).numpy()
        toAdd /= np.sum(toAdd, dim=1)
        np.append(self.features, toAdd, dim=0)

    def reccommend(self, data):
        data /= np.sum(data, dim=1)
        return np.sum(self.features * weights @ data.T, dim=1)
        

if __name__ == '__main__':
    FeatureExtractor()