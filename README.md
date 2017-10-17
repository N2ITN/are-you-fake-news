Fake News Detector
==============

Business Understanding
----------------------

Questions:

-   Can fake news and strongly biased journalism be classified in real time on the web?

-   Can users be notified while browsing news that is misleading,
 deceptive, fabricated, or propaganda?

Data Understanding
------------------

Periodically scrape *n* most recent / popular articles from both reputable and disreputable sources. 



[OpenSources](http://www.opensources.co/) maintains a downloadable database of news sites tagged by: 

- Fake News 
- Satire 
- Extreme Bias 
- Conspiracy Theory 
- Rumor Mill 
- State News 
- Junk Science
- Hate News 
- Clickbait
- Proceed With Caution 
- Political
- Credible

[Media Bias Fact Check](https://mediabiasfactcheck.com/)  maintains an online directory of news sites, categorized by the following political/journalistic tendencies:

- Left bias
- Center left bias
- Least biased
- Center right bias
- RIght bias
- Pro-science
- Conspiracy-pseudoscience
- Questionable sources
- Satire


Data Preparation
----------------

Using the excellent python news scraping package [Newspaper](https://github.com/codelucas/newspaper) this project spiders the tagged websites and extracts new articles to json in mongodb.


Modeling
--------

A variety NLP techniques are used to convert the corpus associated with each tag to vectors and conduct similarity analysis. These will include:

- Non-negative matrix factorization
- Latent dirichlet allocation
- Sentiment analysis
- Lexical / semantic complexity 

The results of these techniques are assembled into an output vector and fed to a classifier for training. Several classifiers will be compared including:

- Logistic regression
- SVM
- Multilayer perceptron DNN


Deployment
----------

The classifier will be hosted on AWS and integrated into a webapp where users could submit urls or text for classification. If possible, the project will expand to a chrome or firefox browser extension.


Evaluation
----------

As new data are always availalbe a continuing metric of sucess will be the evaluation of incoming data.

Additionally, a means of user feedback will be featured in the app.


