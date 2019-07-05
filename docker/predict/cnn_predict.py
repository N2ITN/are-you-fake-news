"""
This module calls the neural network on new data to make predictions.
It resides on AWS Lambda.

"""
import hashlib
import json
import os
import pickle
import warnings
import time

import numpy as np
import tldextract
from tensorflow import keras
from unidecode import unidecode

from add_dict import AddDict

Text = keras.preprocessing.text
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore", category=DeprecationWarning)
model = keras.models.load_model('model.h5')
model._make_predict_function()


def clean(seq):
    if len(seq):
        seq = unidecode(seq)
        return ' '.join(
            Text.text_to_word_sequence(
                seq, filters='''1234567890!"#$%&()*+,-\n./—:;<=>?@[\\]^_`{|}~\t\'“”'''))



def preprocess_articles(article):


    def vectorize(text):
        lookup = json.load(open('lookup234.json'))

        entry = keras.preprocessing.text.text_to_word_sequence(text)

        yield finalize([lookup[word] for word in entry if word in lookup])

    def finalize(entry):
        v_len = 2000

        if len(entry) >= v_len:
            print(len(entry))
            return np.array(entry[-v_len:]).reshape(1, -1)
        return np.array([0 for _ in range(v_len - len(entry))] + entry).reshape(1, -1)

    return list(vectorize(article))


labels = [
    'center', 'conspiracy', 'extreme left', 'extreme right', 'fake news', 'hate', 'high', 'left',
    'left-center', 'low', 'mixed', 'pro-science', 'propaganda', 'right', 'right-center', 'satire',
    'very high'
]


def predict(article):
    preds = model.predict(article)
    label_dict = {i: k for i, k in enumerate(labels)}

    pred_dict = {label_dict[i]: round(float(p), 6) for i, p in enumerate([x for x in preds.flatten()])}
    return pred_dict


def _alphanum(text):
    return ''.join([_ for _ in text if _.isalnum()])


def get_TLD(url):
    return ''.join([char for char in '.'.join(tldextract.extract(url)[-2:]) if char.isalnum()])


def orchestrate(url_article: dict):

    zeroes = predict(preprocess_articles('the ' * 1000))

    def zero(scores: dict):
        res = {}
        for k, v in zeroes.items():

            res[k] = scores[k] - v

        return res

    timestamp = time.strftime("%x")

    results = []
    for url, article in url_article.items():
        article = clean(article)
        results.append({
            'url': hashlib.md5(url.encode('utf-8')).hexdigest(),
            'score': predict(preprocess_articles(article)),
            'timestamp': timestamp,
        })
    return results


# if __name__ == '__main__':

#     entries = orchestrate(json.load(open('../../web/latest.json')))
#     from pprint import pprint
#     pprint(entries)
#     ...
