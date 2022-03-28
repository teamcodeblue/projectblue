import torch
from transformers import BertTokenizer
from torch import nn
from model_defs import ArticleClassifier

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
        

if __name__ == '__main__':
    FeatureExtractor()