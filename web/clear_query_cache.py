"""TOOL: clears query cache for debug mode"""
import os

from pymongo import MongoClient


client = MongoClient()
db = client['newscraper']

print('dropping queries')
db['queries'].drop()

print('removing newspaper cache')
os.system('rm -rf ~/.newspaper_scraper')
