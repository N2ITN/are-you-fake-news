==================
Fake News Detector
==================

In an era increasingly defined by the proliferation of misinformation and polarized politics, it's important for internet users to have context for what's on their screen. This microservice uses natural language processing and deep learning to analyze patterns of bias on any news website in real time. Each time a url is submitted, dozens of the most recent articles are collected and analyzed for a variety of factors, from political bias to journalistic accuracy.


How it works
============

Data Collection
---------------

`OpenSources`_ maintains a downloadable database of news sites with tags related to journalistic accuracy.

`Media Bias Fact Check`_ maintains an online directory of news sites, categorized by the political bias and accuracy.

Using a customized fork of the excellent `Newspaper`_ library this project spiders ~3000 labelled websites for new articles to and stores them by their bias tag in MongoDB. Article texts are minmally preprocessed with unicode cleaning.

Modeling
--------

Using the collected data, a TFIDF vector is fitted on the article collection. A custom-built convolutional neural network is trained in a multi-label classification scheme using a binary crossentropy loss fucntion with a sigmoid output layer. Th model is deployed to AWS Lambda.

Deployment
----------

The website is published via Flask. After a user enters a news site URL, the webserver scans the site for the most 150 recent articles and gathers their URLS. Asynchronously, the text in each url is downloaded using AWS Lambda. The article text is then sent to another AWS Lambda function with the trained neural network model. Results are plotted via matplotlib and rendered in the webpage.

Deeper
------

For a much more detailed discussion of the project please see this living presentation on google slides: https://docs.google.com/presentation/d/1wwnTx0hKB2MJXGPBHbAzElQnCPKH4UFicfnrzsxQG2g/edit?usp=sharing


Open Source
-----------

This is GNU GPL licensed, so anyone can use it as long as it remains open source. 
Anyone who is interested in contributing is welcome to head over to the Data For Democracy repo, where issues are being tracked.
https://github.com/Data4Democracy/are-you-fake-news

Contact
-------

aracel.io

.. _`OpenSources`: http://www.opensources.co/
.. _`Media Bias Fact Check`: https://mediabiasfactcheck.com/
.. _`Newspaper`: https://github.com/codelucas/newspaper
