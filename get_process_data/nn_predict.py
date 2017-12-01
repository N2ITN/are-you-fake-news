import os
import pickle

import numpy as np
from tensorflow import keras

from add_dict import AddDict
from helpers_nlp import LemmaTokenizer

Sequential = keras.models.Sequential
load_model = keras.models.load_model
Tokenizer = keras.preprocessing.text.Tokenizer
Activation = keras.layers.Activation
Dense = keras.layers.Dense
Dropout = keras.layers.Dropout

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

vector_len = 20000

n_classes = 17

corpus_vector = pickle.load(open('./lsa_corpus.pkl', 'rb'))

labels = [
    'extreme left', 'right', 'mixed', 'very high', 'right-center', 'left', 'propaganda', 'satire',
    'extreme right', 'pro-science', 'hate', 'left-center', 'fake news', 'high', 'center', 'low',
    'conspiracy'
]


def transform(text):

    text_ = LemmaTokenizer(text)

    return corpus_vector.texts_to_matrix(text_, mode='tfidf')


def orchestrate(text):

    model = load_model('test_model.h5')

    def chunk_input(text):

        chunks = []
        while text:
            chunks.append(text[:10000])
            text = text[10000:]

        return chunks

    def predict_(chunk):
        X = transform(chunk)

        X = np.array(X.sum(axis=0)).reshape([1, vector_len])

        label_dict = {i: k for i, k in enumerate(labels)}

        preds = model.predict(X)
        np.set_printoptions(precision=4, suppress=True)
        pred_dict = {
            label_dict[i]: round(float(p), 6) for i, p in enumerate([x for x in preds.flatten()])
        }
        return pred_dict

    results = AddDict()
    for r in [predict_(chunk) for chunk in chunk_input(text)]:
        results += r

    return results
