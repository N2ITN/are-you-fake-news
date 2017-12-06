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
    'center', 'conspiracy', 'extreme left', 'extreme right', 'fake news', 'hate', 'high', 'left',
    'left-center', 'low', 'mixed', 'pro-science', 'propaganda', 'right', 'right-center', 'satire',
    'very high'
]


def transform(text):

    text_ = LemmaTokenizer(text)

    return corpus_vector.texts_to_matrix(text_, mode='tfidf')


def orchestrate(text):

    model = load_model('test_model.h5')

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
    zero = predict_(' ')
    print(zero)
    for r in [predict_(chunk) for chunk in text.split(' ||~~|| ')]:
        results += r
    for k, v in results.items():
        results[k] = (v / len(results)) - zero[k]

    return results


if __name__ == '__main__':
    import json
    for x in sorted(
            orchestrate(json.load(open('../web/latest.json'))).items(), key=lambda kv: kv[1],
            reverse=True):
        print(x)