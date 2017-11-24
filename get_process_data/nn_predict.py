import pickle

import numpy as np
import tensorflow as tf

from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential, load_model
from keras.preprocessing.text import Tokenizer

from helpers_nlp import LemmaTokenizer
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

vector_len = 20000

n_classes = 17

corpus_vector = pickle.load(open('./lsa_corpus.pkl', 'rb'))


def transform(text):

    text_ = LemmaTokenizer(text)

    return corpus_vector.texts_to_matrix(text_, mode='tfidf')


def orchestrate(text):

    model = load_model('test_model.h5')

    X = transform(text)

    X = np.array(X.sum(axis=0)).reshape([1, vector_len])

    labels = [
        'extreme left', 'right', 'mixed', 'very high', 'right-center', 'left', 'propaganda', 'satire',
        'extreme right', 'pro-science', 'hate', 'left-center', 'fake news', 'high', 'center', 'low',
        'conspiracy'
    ]

    label_dict = {i: k for i, k in enumerate(labels)}

    preds = model.predict(X)

    pred_dict = {label_dict[i]: p for i, p in enumerate([x for x in preds.flatten()])}

    pretty = sorted(pred_dict.items(), key=lambda kv: kv[1], reverse=True)

    for i, kv in enumerate(pretty):
        # print(kv)
        k, v = kv
        print(k + ' ' * (15 - len(k)), ' ' + '|' * int(float(v) * 100), v)
        if i == 2:
            break

    def pol_spectrum():
        pol_spec = [
            'extreme left', 'left', 'left-center', 'center', 'right-center', 'right', 'extreme right'
        ]
        pol = []
        pol = sorted(
            {
                k + ' ' * (15 - len(k)): ' ' + '|' * int(float(v) * 100) for k, v in pretty
                if k in pol_spec
            }.items(),
            key=lambda kv: pol_spec.index(kv[0].strip()))
        for k, v in pol:
            print(k, v)

    # print(pred_dict)
    # return pred_dict


'''
['left', 'propaganda', 'pro-science', 'fake news', 'mixed', 'high', 'conspiracy', 'satire', 'right-center', 'extreme right', 'center', 'extreme left', 'low', 'hate', 'left-center', 'very high', 'right']
'''