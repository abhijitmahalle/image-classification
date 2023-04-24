# Transfer-Learning

### Project Description:

In this project, I have implemented "Transfer Learning" to train a deep learning model for the task where training data are very limited. Here you are given a data set with ten classes (Ten different monkey
species) with only 140 images per class. First, I trained a simple convolutional neural network using these images and test the accuracy of the model
using the validation set. Then, I used the pre-trained ResNet34 as a feature extractor to perform the transfer learning to boost the efficiency of the model.
Transfer learning significantly improved the efficiency of the model.

### Pipeline

- Here you are given a data set with ten classes (ten different monkey species) with only 140 images per class.
- First, I designed Convolutional Nueral Network and trained it using this data. Because of the low number of training samples, the test accuracy
was lower than expected.
- This is where transfer learning can help. Transfer Learning can be used for deep learning applications where either data or computational power are restricted.
- Next, I used pretrained ResNet34 model as a feature extractor to perform the transfer learning.
- To do this, I removed the last fully connected layers of the pretrained model and replace it with the untrained fully connected layer s to classify the
monkey species. 
- During training, I freezed the convolutional layer parameters so that they remain the same and only update the fully connected layers at the end. 
In this way, the convolutional layers act as generalized feature extractors that have already been pretrained on millions of other images (that werent 
necessarily all monkeys) while the fully connected layers are able to take these features and classify our images. 
- This showed substential boost in accuracy despite having the same amount of training sample. 
- To further boost the performance of the network, I unfreezed the convolutional layers and trained for a few more epochs with a small step size to 
fine tune the network to extract even more predictive power.

### Dataset

[10 monkey species](https://www.kaggle.com/slothkong/10-monkey-species/home)

### Results

1. Performance of the CNN without Transfer Learning

      | Sr No |  Hyperparameters | Values/Type |
      |:-----:|:----------------:|:-----------:|
      |   1   |     Optimizer    |     Adam    |
      |   2   |   Learning Rate  |    10<sup>-5</sup>    |
      |   3   | Number of Epochs |     100     |
      |   4   |    Batch Size    |      16     |

![adam_100epoch_10e5_16batch](https://user-images.githubusercontent.com/90370308/216736119-41ea2444-8a91-4406-97ab-63aef84122f4.png)
 - Testing Accuracy: 45.58%
 
 2. Performance with the Transfer learning with only Fully connected layer tuned
 
      | Sr No |  Hyperparameters | Values/Type |
      |:-----:|:----------------:|:-----------:|
      |   1   |     Optimizer    |     Adam    |
      |   2   |   Learning Rate  |    10<sup>-5</sup>    |
      |   3   | Number of Epochs |     100     |
      |   4   |    Batch Size    |      16     |
      
![Adam_8_train](https://user-images.githubusercontent.com/90370308/216736325-226f3dff-5361-4f9e-92c0-23cb65d7ee20.png)
 - Testing Accuracy: 95.58%
 
 3. Performance with the Transfer learning with all the layer tuned
 
      | Sr No |  Hyperparameters | Values/Type |
      |:-----:|:----------------:|:-----------:|
      |   1   |     Optimizer    |     Adam    |
      |   2   |   Learning Rate  |    10<sup>-5</sup>    |
      |   3   | Number of Epochs |     100     |
      |   4   |    Batch Size    |      16     |
 
![1](https://user-images.githubusercontent.com/90370308/216736555-d27fe0e6-7ebb-4c71-9f46-5a15eef78628.png)
- Testing Accuracy: 98.38%

## Requirement
Python 2.0 or above

## License

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Copyright (c) Feb 2023 Pradip Kathiriya
