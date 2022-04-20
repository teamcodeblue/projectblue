#adapted from https://towardsdatascience.com/text-classification-with-bert-in-pytorch-887965e5820f

from torch import nn
from transformers import BertModel

class ArticleClassifier(nn.Module):
    def __init__(self, dropout=0.5):
        super(ArticleClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-cased').to("cuda:0")
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 5)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, cls = self.bert(input_ids= input_id, attention_mask=mask,return_dict=False)

        dropout_output = self.dropout(cls)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)

        return final_layer
