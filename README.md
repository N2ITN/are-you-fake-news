# Fake News Detector

In an era increasingly defined by the proliferation of misinformation and polarized politics, it's important for internet users to have context for what's on their screen. This microservice uses natural language processing and deep learning to analyze patterns of bias on any news website in real time. Each time a url is submitted, dozens of the most recent articles are collected and analyzed for a variety of factors, from political bias to journalistic accuracy.

# Microservice Architecture

Each of the directories in the `./Docker/` folder contain the ingredients for a microservice. These services work together to form the app. Microservices in this app are comprised of serveral elements which make for a stable and well-defined function unit of code.

```
Docker/
    example_microservice/

        README.MD - High level overview
            Purpose
                Explain functionality
            Connections
                What services does this connect to, how, and why
            API Definition
                Outline service agreement + protocol

        Unit tests - Formally test the API Definition

        Dockerfile
            Lightweight officially supported image
            Specified version numbers of libraries

        Source Code
            Design
                Efficient, flexible, lightweight
            Quality
                Organized, commented, formatted.


```

---

# Front end services

These microservices comprise the production website for serving predicitons to the user.

### Control Flow

This is the controller of logic for the production website. It directs the backend execution of web requests initiated by user activity.

### Web

The web interface. Uses flask, gninx, gunicorn to host the dynamic and static pages.

### Web scraper

Several small functions for gathering text and metadata from news sites. Includes a domain spiderer to inventory article urls on a site, and map/reduce scraper pattern for asyncronous web scraping of the article urls.

### Plotter

Matplotlib and code for generating plots given prediction data.

### Predict

Lightweight tensorflow/keras NLP container for generating predictions from text.

---

## Data Persistence

---

### Mongo

Contains a mongoDB image with a few custom queries. Serves as the central source of state on the site.

---

## Model Training

---

These services are used to collect data from labelled sources for training the convolutional neural net. The resulting model files are then used in the production site.

### Gather Data

Downloads articles from websites into a common format. Articles are stored in MongoDB.

### Train

Trains model using collected data and generates neural network weights, word vectors.

---

# Site Background

## Data Collection

---

[OpenSources](http://www.opensources.co/) maintains a downloadable database of news sites with tags related to journalistic accuracy.

[Media Bias Fact Check](https://mediabiasfactcheck.com/) maintains an online directory of news sites, categorized by the political bias and accuracy.

Using a customized fork of the excellent [Newspaper](https://github.com/codelucas/newspaper) library this project spiders ~3000 labelled websites for new articles to and stores them by their bias tag in MongoDB. Article texts are minmally preprocessed with unicode cleaning.

## Modeling

---

Using the collected data, a TFIDF vector is fitted on the article collection. A custom-built convolutional neural network is trained in a multi-label classification scheme using a binary crossentropy loss fucntion with a sigmoid output layer. Th model is deployed to AWS Lambda.

## Deployment

---

The website is published via Flask. After a user enters a news site URL, the webserver scans the site for the most 150 recent articles and gathers their URLS. Asynchronously, the text in each url is downloaded using AWS Lambda. The article text is then sent to another AWS Lambda function with the trained neural network model. Results are plotted via matplotlib and rendered in the webpage.

## Deeper

---

For a much more detailed discussion of the project please see this living presentation on google slides: https://docs.google.com/presentation/d/1wwnTx0hKB2MJXGPBHbAzElQnCPKH4UFicfnrzsxQG2g/edit?usp=sharing

## Open Source

This is GNU GPL licensed, so anyone can use it as long as it remains open source.
Anyone who is interested in contributing is welcome to head over to the Data For Democracy repo, where issues are being tracked.
https://github.com/Data4Democracy/are-you-fake-news

## Contact

aracel.io
