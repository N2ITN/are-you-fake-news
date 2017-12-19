#!/usr/bin/env bash

## This is the pipeline to scrape data and train a model.

## Uncomment to re-scrape mediabiasfactcheck.com for website bias labels
## and recreate database of website labels
#python3 labels_MBFC.py && python3 join_source_lists.py &&


## Uncomment to delete scraped articles
#python3 mongo_driver.py --kill articles &&

## Uncomment to scrape articles from websites in database, preprocess scraped articles,

#python3 webcrawler.py && python3 lemmatize_articles.py


## Uncomment to create new vocabulary vector
#cd ../_nlp_lambda/code/ && python3 NLP_nn.py && cd ../../get_process_data && 


## Uncomment to re-train neural net
#cd ../_nlp_lambda/code/  && python3 nn_playground.py && cd ../../get_process_data && 
