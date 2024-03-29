# -*- coding: utf-8 -*-
"""simple_cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15A7bY5VIwLyWR9ZKGvmpmUymSGNLADr8
"""

from google.colab import drive
drive.mount('/content/drive')

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

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

train_set = torchvision.datasets.ImageFolder('/content/drive/MyDrive/828C/proj2/part2/data/monkey_species/training', transform=train_transforms)
test_set = torchvision.datasets.ImageFolder('/content/drive/MyDrive/828C/proj2/part2/data/monkey_species/validation', transform=test_transforms)

plt.imshow(train_set[0][0].permute(1,2,0))

BATCH_SIZE = 64

torch.manual_seed(0)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
torch.manual_seed(0)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=2)
        self.batch_32 = nn.BatchNorm2d(32)

        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=2)
        self.batch_64 = nn.BatchNorm2d(64)

        self.conv3 = nn.Conv2d(in_channels=64,out_channels=128, kernel_size=5, padding=2)
        self.batch_128 = nn.BatchNorm2d(128)

        self.conv4 = nn.Conv2d(in_channels=128,out_channels=256, kernel_size=5, padding=2)
        self.batch_256 = nn.BatchNorm2d(256)

        self.conv5 = nn.Conv2d(in_channels=256, out_channels=512, kernel_size=7, padding=3)
        self.batch_512 = nn.BatchNorm2d(512)

        self.max_pool = nn.MaxPool2d(kernel_size=2)
        self.dropout = nn.Dropout(p=0.45)

        self.fc1 = nn.Linear(in_features=512*8*8, out_features=64)
        self.batch_fc = nn.BatchNorm1d(64)

        self.out = nn.Linear(in_features=64, out_features=10)

    
    def forward(self, x):

        x = self.conv1(x)
        x = self.batch_32(x)
        x = F.relu(x)
        x = self.max_pool(x)
        x = self.dropout(x)

        x = self.conv2(x)
        x = self.batch_64(x)
        x = F.relu(x)
        x = self.max_pool(x)
        x = self.dropout(x)

        x = self.conv3(x)
        x = self.batch_128(x)
        x = F.relu(x)
        x = self.max_pool(x)
        x = self.dropout(x)

        x = self.conv4(x)
        x = self.batch_256(x)
        x = F.relu(x)
        x = self.max_pool(x)
        x = self.dropout(x)

        x = self.conv5(x)
        x = self.batch_512(x)
        x = F.relu(x)
        x = self.max_pool(x)
        x = self.dropout(x)

        x = self.fc1(x.view(-1, 512*8*8))
        x = self.batch_fc(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.out(x)

        return x

net = Net()

EPOCHS = 60
LEARNING_RATE = 0.001
optimizer = torch.optim.Adam(net.parameters(), lr=LEARNING_RATE, weight_decay=0.001)
criterion = nn.CrossEntropyLoss()

def train():
    train_loss = []
    test_loss = []
    train_accuracy_list = []
    test_accuracy_list = []

    for epoch in range(EPOCHS):
        running_loss = 0.0
        running_test_loss = 0.0
        correct_predictions = 0.0

        net.train()
        for (data, target) in train_loader:
            optimizer.zero_grad()
            output = net(data.view(BATCH_SIZE, 3, img_crop, img_crop))
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            running_loss += loss.detach().item()

            index = output.max(dim=1)[1]
            correct_predictions += (index == target).sum().detach().item()
        
        train_accuracy = 100*(correct_predictions / (len(train_loader)*BATCH_SIZE))
        train_accuracy_list.append(train_accuracy)

        correct_predictions = 0.0

        with torch.no_grad():
            net.eval()
            for (data, target) in test_loader:
                output = net(data.view(BATCH_SIZE, 3, img_crop, img_crop))
                loss = criterion(output, target)
                running_test_loss += loss.detach().item()

                index = output.max(dim=1)[1]
                correct_predictions = correct_predictions + (index == target).sum().detach().item()

        avg_train_loss = running_loss / len(train_loader)
        train_loss.append(avg_train_loss)

        avg_test_loss = running_test_loss / len(test_loader)
        test_loss.append(avg_test_loss)

        test_accuracy = 100*(correct_predictions / (len(test_loader)*BATCH_SIZE))
        test_accuracy_list.append(test_accuracy)

        print('Epoch {}, Train Loss: {:.4f}, Test Loss: {:.4f}, Train Accuracy: {:.3f}, Test Accuracy: {:.3f}'.format(epoch+1, avg_train_loss, avg_test_loss, train_accuracy, test_accuracy))

    return train_loss, test_loss, train_accuracy_list, test_accuracy_list

train_loss, test_loss, train_accuracy_list, test_accuracy_list = train()

plt.plot(range(1, 29), train_loss, color='b', label='Training loss')
plt.plot(range(1, 29), test_loss, color='r', label='Test loss')
plt.xlabel('Number of epochs')
plt.ylabel('Cross entropy loss')
plt.title('Simple CNN on monkey dataset - Loss vs No. of Epochs')
plt.legend()
plt.show()