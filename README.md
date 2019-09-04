# Synthetic Data GAN Capstone
This project can be broken down into two primary pieces:

1. Analyze a variety of well-known data sets and design Generative Adversarial Networks (GANs) capable of generating realistic looking data from them.

I have selected a variety of data sets with the intention of learning how to overcome various obstacles presented when training GANs, such as extremely small training data, categorical data, imbalanced classes, audio signals, and images. 

The goal is to be able to train generative models with a deep enough understanding of the underlying data distribution so that a model trained on only fake data can outperform models trained on the original real data. This goal has been achieved, and there are lots of ways for a user to interact with the models contained within this repository in order to learn about GANs and generate better models.

2. Build a containerized web app that can employ these flexible GANs to generate data for a user from any data set.

So far the web app is only capable of handling tabular data sets, but functionality for image data sets is coming soon, and a stretch goal is to incorporate NLP functionality.

## Motivation
The three most important applications of generating synthetic data are as follows:

1. Data augmentation for imbalanced data sets
2. Data augmentation for data sets of insufficient size to train high quality models
3. Ability to share valuable training data that may not otherwise be shareable due to confidentiality or privacy concerns.

## Datasets Included
1. Iris (UCI Repository, https://archive.ics.uci.edu/ml/machine-learning-databases/iris/)
2. Wine (UCI Repository, https://archive.ics.uci.edu/ml/machine-learning-databases/wine/)
3. Titanic (Kaggle, https://www.kaggle.com/c/titanic)
4. LANL Earthquake Acoustic Signal Data (Kaggle, https://www.kaggle.com/c/LANL-Earthquake-Prediction/overview)
5. MNIST (Yann LeCun's website, http://yann.lecun.com/exdb/mnist/)
6. Fashion MNIST (Zalando Research, https://github.com/zalandoresearch/fashion-mnist)

## Features
1. Framework to quickly and easily prototype a variety of GAN architectures on a variety of data sets.
2. Tools to peek into the inner workings of the GAN training process in order to diagnose issues and improve performance.
3. Web app that is easily deployable with only a few lines of code and minimal software required.

## Getting Started
1. Fork the project
2. Clone the repository: `$git clone https://github.com/Atrus619/Synthetic_Data_GAN_Capstone`
3. Create a virtual environment: `$python3 -m venv /path/to/new/virtual/env`
4. Install dependencies: `$pip install -r requirements.txt`

While it helps to have a GPU, most of these models will train on a CPU without a noticeable decrease in computation time. In fact, depending on your CPU, some of these models are actually trained faster on a CPU.

The code contains helper functions to automatically download the data sets and set up folders for running experiments. 
Add information about virtual environment and loading dependencies

## How to use the framework?
While all of the code is yours to explore, I recommend starting out by checking out the notebooks included in the scripts folder. 
1. The Exploration Notebooks walk through the EDA of each data set, as well as some of the cleaning/preprocessing involved before training the models.
2. The CGAN Notebooks walk through how to train the successful GAN models. 
3. From there, you are free to dive into the model architectures themselves (contained in the models folder), as well as the various helper functions used to visualize and better understand the training process and model quality.

## How to run the app?
The app has been decomposed into Docker containers, and these containers are all available on Docker's cloud service.
If you wish to expose the web app to the internet, you will need to install ngrok:

`make install ngrok` OR `sudo snap install ngrok`

With ngrok installed, to run the app in a single line of code:

`./deploy.sh`

To run the app locally in a dev environment (not containerized), you can run (you may want to change DOCKERIZED in CSDGAN/utils/constants.py to FALSE to do this):

`./dev_deploy.sh`

Feel free to check out the Makefile for other relevant commands:

`make help`

## How to Contribute
I would love to hear from users who were able to modify the architectures or training hyperparameters to produce better performing models. Additionally, proposing new data sets and even uploading implementations that are successful would be a great contribution!

## Credits
I would like to give credit to the countless open source researchers and bloggers who made this work possible by selflessly sharing their work so that I could learn from their experiences.

## License
MIT License
