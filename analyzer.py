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
    tags = defaultdict(list)
    for j in iglob('./scraped/*.json'):
        j_ = json.load(open(j))
        '''for _ in j_['Articles']:
            words = _[list(_.keys())[0]]['text'].split()
            i += 1
            # cleaned = list(filter(lambda x: x.lower() not in set(stopWords), words))
            for flag in j_['Meta']['Flags']:
                if len(words):
                    tags[flag].extend(words)'''

        for _ in j_['Articles']:
            title = list(_.keys())[0]
            keywords = _[title]['keywords']
            words = [title] + keywords
            i += 1
            for flag in j_['Meta']['Flags']:
                if len(words):
                    tags[flag].extend(words)

    return dict(tags), 'tags'


def topic_modeler(tag, n_top_words=10, n_topics=10):
    blacklist = ['http', 'https', 'www', 'videodurationmomentjs']
    text_ = list(filter(lambda x: x not in blacklist and x, tags[tag]))
    vectorizer = text.CountVectorizer(
        input=text_, stop_words='english', min_df=3, max_df=1.0, max_features=5000)
    dtm = vectorizer.fit_transform(text_)
    # nmf = NMF(
    # n_components=n_topics,).fit(dtm)
    feature_names = vectorizer.get_feature_names()
    print(tag, len(text_), 'words', '\n')
    print(TextBlob(' '.join(tags[tag])).sentiment, '\n')

    lda = LatentDirichletAllocation(
        n_topics=n_topics, max_iter=10, learning_method='batch', learning_offset=50.)
    lda.fit(dtm)
    for topic_idx, topic in enumerate(lda.components_):
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))


index_by_tag()
tags = json.load(open('tags.json'))
print(list(tags.keys()), '\n')
tag = 'real'
topic_modeler(tag)


def sentiment(t):
    return
