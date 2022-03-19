# -*- coding: utf-8 -*-
"""content_rec

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LYzaJrH53no05bB14Ija1viMajLkmCc3

dataset used: https://www.kaggle.com/sainijagjit/bbc-dataset
"""

"""
input format:
    content_rec [path of dataset] [output path]
optional parameters:
    (all followed by a number and after required params)
    -epochs
    -batch_size
    -lr
    -
    
    
"""

import torch
from torch import nn
from torch import optim
import pandas as pd
from transformers import BertModel
from transformers import BertTokenizer
import numpy as np
from tqdm import tqdm
from model_defs import ArticleClassifier
import sys

argv = sys.argv

if len(argv) < 2:
    print('arg error')

input_path = argv[1]
dest = argv[2]

epochs = 5
lr = 1e6

for i in range(3,len(argv),2):
    flag = argv[i]
    if flag == '-epochs':
        epochs = argv[i+1]
    if flag == 'lr':
        epochs = argv[i+1]
    if flag == '-batch_siz':
        epochs = argv[i+1]
    if flag == '-epochs':
        epochs = argv[i+1]


labels = {'business':0,
          'entertainment':1,
          'sport':2,
          'tech':3,
          'politics':4
          }
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

class BBCDataset(torch.utils.data.Dataset):
  def __init__(self, df):
    #labels_arr = [labels[label] for label in df['Category']]
    self.labels = [labels[label] for label in df['Category']]
    self.texts = [tokenizer(text, padding='max_length', max_length = 512, truncation=True, return_tensors="pt") for text in df['Text']]
  
  def __len__(self):
    return len(self.texts)

  def __getitem__(self, idx):
    return self.texts[idx], np.array(self.labels[idx])

def train(model, train_dataset, test_dataset, batch_size, epochs, optimizer):
  train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=4, shuffle=True)
  test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=4)

  device = torch.device("cuda" if torch.torch.cuda.is_available() else "cpu")

  model.to(device)

  criterion = nn.CrossEntropyLoss()

  for epoch in range(epochs):
    train_total_loss = 0
    train_total_correct = 0
    print('Epoch: ', epoch + 1)
    for input, label in tqdm(train_loader):
      label = label.to(device)

      output = model(input['input_ids'].squeeze(1).to(device), input['attention_mask'].to(device))

      loss = criterion(output, label)

      model.zero_grad()
      loss.backward()
      optimizer.step()

      train_total_loss += loss.item()
      
      test_total_correct = torch.sum(torch.argmax(output, dim=1) == label).item()
    print(' Training Loss: ', train_total_loss, 'Traing Accuracy:', train_total_correct / len(test_dataset))
    
    test_total_loss = 0
    test_total_correct = 0
    with torch.no_grad():
      for input, label in tqdm(test_loader):
        label = label.to(device)

        output = model(input['input_ids'].squeeze(1).to(device), input['attention_mask'].to(device))

        loss = criterion(output, label)
        test_total_loss += loss.item()
        
        test_total_correct += torch.sum(torch.argmax(output, dim=1) == label).item()
    
    
    print(' Test Loss: ', test_total_loss, 'Test Accuracy:', test_total_correct / len(test_dataset))

raw_data = pd.read_csv(input_path)


train_data = raw_data.sample(frac=0.8, random_state=1216)
test_data = raw_data.drop(train_data.index)

train_dataset = BBCDataset(train_data)
test_dataset = BBCDataset(test_data)

model = ArticleClassifier()
optimizer = torch.optim.Adam(model.parameters(), lr=2e-6)

train(model, train_dataset, test_dataset, 4, 4, optimizer)

torch.save(model, output)
