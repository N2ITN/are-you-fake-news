''' Does NLP stuff '''

import json
from collections import Counter, defaultdict
from glob import iglob

import numpy as np
import sklearn.feature_extraction.text as text
from nltk.corpus import stopwords
from sklearn.decomposition import NMF, LatentDirichletAllocation

from helpers import j_writer
from textblob import TextBlob

stopWords = set(stopwords.words('english'))


@j_writer
def index_by_tag():
    i = 0
    arcticles_tagged = defaultdict(list)
    for j in iglob('./scraped/*.json'):
        j_ = json.load(open(j))
        for _ in j_['Articles']:
            title = list(_.keys())[0]
            keywords = _[title]['keywords']
            words = [title] + keywords
            i += 1
            for flag in j_['Meta']['Flags']:
                if len(words):
                    arcticles_tagged[flag].extend(words)

    return dict(arcticles_tagged), 'arcticles_tagged'


import mongo_driver
articles = mongo_driver.get_all('articles')


class topic_modeler:

    def __init__(self, flag, arcticles_tagged, n_top_words=10, n_topics=5):

        self.flag = flag
        self.n_top_words = n_top_words
        self.n_topics = n_topics
        self.text_ = arcticles_tagged

    def fit(self, model='nmf'):
        vectorizer = text.CountVectorizer(
            input=self.text_, stop_words='english', min_df=3, max_df=.95, max_features=5000)
        dtm = vectorizer.fit_transform(self.text_)
        self.feature_names = vectorizer.get_feature_names()

        if model == 'nmf':
            model = NMF(
                n_components=self.n_topics,).fit(dtm)
        elif model == 'lda':
            model = LatentDirichletAllocation(
                n_topics=n_topics, max_iter=10, learning_method='batch', learning_offset=50.)

        self.model = model.fit(dtm)
        self.show()

    def sentiment(self):
        print(TextBlob(' '.join(self.arcticles_tagged[tag])).sentiment, '\n')

    def show(self):
        print(self.flag)
        for topic_idx, topic in enumerate(self.model.components_):
            print(" ".join([self.feature_names[i] for i in topic.argsort()[:-self.n_top_words - 1:-1]]))


''' Getting docs by arcticles_tagged'''


def from_json():
    arcticles_tagged = json.load(open('arcticles_tagged.json'))
    print(arcticles_tagged.keys())
    print(arcticles_tagged['Political'])


def from_mongo():
    from group_articles_by_flag import unique_flags
    for flag in unique_flags():

        flag_articles = mongo_driver.db['articles_by_flag'].find({'flag': flag})

        yield flag, (doc['article'] for doc in flag_articles)


flag_counts = mongo_driver.flag_counts()

for i, _ in enumerate(from_mongo()):

    f, d = _
    if flag_counts[f] < 150:
        continue

    if i > 0:
        test = topic_modeler(f, d)
        test.fit()
        print()

test.fit()
