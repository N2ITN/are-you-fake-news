import joblib
import mongo_driver
from helpers import LemmaTokenizer

from models import Model

corpus_vector = joblib.load('./lsa_corpus.pkl').vectorizer


def transform(text):

    text_ = LemmaTokenizer(text)
    return corpus_vector.transform(text_)


def vectorize_article():

    def corpus_gen():
        for i, _ in enumerate(mongo_driver.get_all('articles_cleaned')):

            if _['article']:
                yield _['flag'], _['article']

    for flag, article in corpus_gen():

        try:
            yield flag, transform(' '.join(article))
        except Exception as e:
            raise e


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation


def define_model():
    model = Sequential()
    model.add(Dense(512, input_shape=(10000,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(18))
    model.add(Activation('softmax'))
    return model


def run_net():

    model = define_model()

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    history = model.fit(
        x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.1)
    score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)
