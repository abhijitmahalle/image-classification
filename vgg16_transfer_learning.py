# -*- coding: utf-8 -*-
"""vgg16_transfer_learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TKtRhnDi0vmepjjvWd5P4PlhNHPSHjWm
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import models
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import random
import tqdm

vgg16 = models.vgg16(pretrained=True)

for param in vgg16.features.parameters():
    param.requires_grad = False

# Newly created modules have require_grad=True by default
num_features = vgg16.classifier[6].out_features
features = list(vgg16.classifier.children())
features.extend([nn.ReLU(inplace=True)])
features.extend([nn.Dropout(p=0.5, inplace=False)])
features.extend([nn.Linear(num_features, 10, bias=True)]) # Add our layer with 10 outputs
vgg16.classifier = nn.Sequential(*features) # Replace the model classifier

img_size = 380
img_crop = 256

#Applying Transformation
train_transforms = transforms.Compose([transforms.Resize((img_size,img_size)),
                                transforms.CenterCrop(img_crop),
                                transforms.RandomHorizontalFlip(), 
                                transforms.ToTensor()])

test_transforms = transforms.Compose([transforms.Resize((img_size,img_size)),
                                      transforms.CenterCrop(img_crop),
                                      transforms.ToTensor()])

train_set = torchvision.datasets.ImageFolder('/content/monkey_species/training/training', transform=train_transforms)
test_set = torchvision.datasets.ImageFolder('/content/monkey_species/validation/validation', transform=test_transforms)

BATCH_SIZE = 64

torch.manual_seed(0)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
torch.manual_seed(0)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)

EPOCHS = 10
LEARNING_RATE = 0.001
optimizer = torch.optim.Adam(vgg16.parameters(), lr=LEARNING_RATE, weight_decay=0.001)
criterion = nn.CrossEntropyLoss()

def train(): 
    train_loss = []
    test_loss = []
    train_accuracy = []
    test_accuracy = []

    for epoch in range(EPOCHS):
        running_loss = 0.0
        running_test_loss = 0.0
        correct_predictions = 0.0

        vgg16.train()
        for (data, target) in train_loader:
            optimizer.zero_grad()
            output = vgg16(data.view(BATCH_SIZE, 3, img_crop, img_crop))
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            running_loss += loss.detach().item()

            index = output.max(dim=1)[1]
            correct_predictions = correct_predictions + (index == target).sum().detach().item()
        
        train_acc = 100*(correct_predictions / (len(train_loader)*BATCH_SIZE))
        train_accuracy.append(train_acc)

        correct_predictions = 0.0

        with torch.no_grad():
            vgg16.eval()
            for (data, target) in test_loader:
                output = vgg16(data.view(BATCH_SIZE, 3, img_crop, img_crop))
                loss = criterion(output, target)
                running_test_loss += loss.detach().item()

                index = output.max(dim=1)[1]
                correct_predictions = correct_predictions + (index == target).sum().detach().item()

        avg_train_loss = running_loss / len(train_loader)
        train_loss.append(avg_train_loss)

        avg_test_loss = running_test_loss / len(test_loader)
        test_loss.append(avg_test_loss)

        accuracy = 100*(correct_predictions / (len(test_loader)*BATCH_SIZE))
        test_accuracy.append(accuracy)
        print('Epoch {}, Train Loss: {:.4f}, Test Loss: {:.4f}, Train Accuracy: {:.3f}, Test Accuracy: {:.3f}'.format(epoch+1, avg_train_loss, avg_test_loss, train_acc, accuracy))

    return train_loss, test_loss, train_accuracy, test_accuracy

train_loss, test_loss,  train_accuracy, test_accuracy = train()

plt.plot(list(range(1, EPOCHS + 1)), train_loss, color='b', label='Training loss')
plt.plot(list(range(1, EPOCHS + 1)), test_loss, color='r', label='Test loss')
plt.xlabel('Number of epochs')
plt.ylabel('Cross Entropy Loss')
plt.title('VGG16 - Transfer Learning - Loss vs No. of epochs')
plt.legend()
plt.savefig('/content/VGG16_loss_2.png')
plt.show()

for param in vgg16.features.parameters():
    param.requires_grad = True

EPOCHS = 5
LEARNING_RATE = 0.0001
optimizer = torch.optim.Adam(vgg16.parameters(), lr=LEARNING_RATE, weight_decay=0.001)
criterion = nn.CrossEntropyLoss()

train_loss, test_loss, train_accuracy_list, test_accuracy_list = train()

plt.plot(list(range(1, EPOCHS + 1)), train_loss, color='b', label='Training loss')
plt.plot(list(range(1, EPOCHS + 1)), test_loss, color='r', label='Test loss')
plt.xlabel('Number of epochs')
plt.ylabel('Cross Entropy Loss')
plt.title('VGG16 - Transfer Learning - Loss vs No. of epochs')
plt.legend()
plt.savefig('/content/VGG16_loss_3.png')
plt.show()

plt.plot(list(range(1, EPOCHS + 1)), train_accuracy_list, color='b', label='Training accuracy')
plt.plot(list(range(1, EPOCHS + 1)), test_accuracy_list, color='r', label='Test accuracy')
plt.xlabel('Number of epochs')
plt.ylabel('Accuracy in %')
plt.title('VGG16 - Transfer Learning - Accuracy vs No. of epochs')
plt.legend()
plt.savefig('/content/VGG16_accuracy_3.png')
plt.show()
