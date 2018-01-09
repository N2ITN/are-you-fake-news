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

# Path Forward

Next steps.

## Easy

Add interface option for per article submission
Add interface option for raw text submission
Set up automatic data refresh, including scraping, cleaning, retraining model, and deployment of Lambda function (hinges on AWS API Gateway integration).

## Medium

Move plotting function from webserver to Lambda
Move live site crawler from webserver to Lambda

## More Involved

### Persistence

    Set up data persistence for returned queries. After an article is classified, the scores can be stored in MongoDB along with the article URL and the parent website. Adding this layer will allow for several improvements:
        * Much inscreased speed in searching an individual website can used cached results aggregate or stream in newer articles in the background
        * It will allow for a multitude of interesting data visualizations, including:  comparing websites, showing change in bias over time for one or more sites, highest and lowest bias and distribution, and much more.
