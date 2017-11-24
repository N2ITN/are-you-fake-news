import pickle

import numpy as np
import tensorflow as tf
from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential, load_model
from keras.preprocessing.text import Tokenizer

from helpers_nlp import LemmaTokenizer

vector_len = 15000

n_classes = 17

corpus_vector = pickle.load(open('./lsa_corpus.pkl', 'rb'))


def transform(text):

    text_ = LemmaTokenizer(text)

    return corpus_vector.texts_to_matrix(text_, mode='tfidf')


def define_model():

    try:
        return load_model('test_model.h5')
    except Exception as e:
        print(e)
    model = Sequential()
    model.add(Dense(64, input_shape=(vector_len,)))
    model.add(Activation('relu'))
    Dropout(.3)

    model.add(Dense(
        n_classes,))
    model.add(Activation('sigmoid'))

    return model


def orchestrate(text):
    print('imported keras libs ')
    model = define_model()

    X = transform(text)

    X = np.array(X.sum(axis=0)).reshape([1, 15000])

    labels = [
        'extreme left', 'right', 'mixed', 'very high', 'right-center', 'left', 'propaganda', 'satire',
        'extreme right', 'pro-science', 'hate', 'left-center', 'fake news', 'high', 'center', 'low',
        'conspiracy'
    ]

    label_dict = {i: k for i, k in enumerate(labels)}

    preds = model.predict(X)

    pred_dict = {label_dict[i]: str(p) for i, p in enumerate([x for x in preds.flatten()])}

    pretty = sorted(pred_dict.items(), key=lambda kv: kv[1], reverse=True)
    print()
    for kv in pretty:
        print(kv)
    print()

    return pred_dict


if __name__ == '__main__':
    print(
        orchestrate(
            ''' President Tump released his Thanksgiving message to the country Thursday morning. The message included a full-throated defense of his policies, the military and the future of the country. The president mentioned “God” nine times and “prayer” twice in his message.

Trump asked the nation multiple times to “thank God” in “prayer” and recalled the story of the first Thanksgiving, where pilgrims and Amerindians sat down together to enjoy a meal and thank God for the bounty of the harvest in the new land.

The president also recalled his predecessors, George Washington and Abraham Lincoln, who were instrumental in designating Thanksgiving as national holiday.

“Today we give thanks for all of the pilgrims, pioneers, and patriots who have gone before us, and for all those warriors that have kept us safe and free,” he said.
.'''))
