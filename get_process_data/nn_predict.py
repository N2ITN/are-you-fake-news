import joblib
import keras
import numpy as np
from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential, load_model

from helpers_nlp import transform

#TODO Get Scikit learn in package to vectorize text
corpus_vector = joblib.load('./lsa_corpus.pkl').vectorizer

vector_len = 10000

n_classes = 17


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
    model.add(Activation('softmax'))

    return model


def orchestrate(text):
    model = define_model()

    text_xform = transform(text)
    text_xform = np.array(text_xform.todense().sum(axis=0).flatten())

    labels = [
        'extreme left', 'right', 'mixed', 'very high', 'right-center', 'left', 'propaganda', 'satire',
        'extreme right', 'pro-science', 'hate', 'left-center', 'fake news', 'high', 'center', 'low',
        'conspiracy'
    ]

    label_dict = {i: k for i, k in enumerate(labels)}

    preds = model.predict(text_xform)

    pred_dict = {label_dict[i]: p for i, p in enumerate([x for x in preds.flatten()])}
    return pred_dict


if __name__ == '__main__':
    print(orchestrate('liberal conspiracy russia aliens ufo'))
