# Fake News Detector

In an era increasingly defined by the proliferation of misinformation and polarized politics, it's important for internet users to have context for what's on their screen. This microservice uses natural language processing to analyze patterns of bias on any news website in real time. Each time a url is submitted, dozens of the most recent articles are collected and analyzed for a variety of factors, from political bias to journalistic accuracy.

# How it works

## Data Collection

---

[OpenSources](http://www.opensources.co/) maintains a downloadable database of news sites with tags related to journalistic accuracy.

[Media Bias Fact Check](https://mediabiasfactcheck.com/) maintains an online directory of news sites, categorized by the political bias and accuracy.

Using a customized fork of the excellent [Newspaper](https://github.com/codelucas/newspaper) library this project spiders ~3000 labelled websites for new articles to and stores them by their bias tag in MongoDB. Text is preprocessed with unicode cleaning, stemming using NLTK.

## Modeling

---

Using the collected data, a TFIDF vector is fitted on a corpus the scraped articles (the article count started aroun 45k but continues to rise as more articles are collected periodicaly ). A custom neural network with 2 hidden layers is trained in a multi-label classification scheme using binary crossentropy with a sigmoid output layer. This model is pickled and deployed to AWS Lambda.

## Deployment

---

The website is published via Flask. After a user enters a news site URL, the webserver scans the site for the most 100 recent articles and gathers their URLS. This list of URLs is sent asynchronously to an AWS Lambda instance to retreive the text of the 100 articles. The article text is then sent to the AWS Lambda function with the trained neural network model. Finally, the results are plotted via matplotlib and rendered in the webpage.

![alt text](web/static/img/workflow_bg.png "flow")

## Deeper

---

For a much more detailed discussion of the project please see this living presentation on google slides: https://docs.google.com/presentation/d/1wwnTx0hKB2MJXGPBHbAzElQnCPKH4UFicfnrzsxQG2g/edit?usp=sharing
