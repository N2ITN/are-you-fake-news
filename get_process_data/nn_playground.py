from itertools import islice

import keras
import numpy as np
from keras import backend as K
from keras.layers import Activation, Dense, Dropout
from keras.metrics import top_k_categorical_accuracy
from keras.models import Sequential, load_model
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint

from vectorizer_nn import vectorize_article

n_classes = 17

labels = [
    'extreme left', 'right', 'mixed', 'very high', 'right-center', 'left', 'propaganda', 'satire',
    'extreme right', 'pro-science', 'hate', 'left-center', 'fake news', 'high', 'center', 'low',
    'conspiracy'
]

label_dict = {k: i for i, k in enumerate(labels)}


class X_shape:
    shape = None


vector_len = 50000

articles = vectorize_article()


def generator():
    print('vectorized article')
    source = articles
    print('produced source')
    labels = dict()

    batch_size = 64
    batch_features = np.zeros((batch_size, vector_len,))
    batch_labels = np.zeros((batch_size, n_classes))
    while True:
        for i in range(batch_size):

            y, X = next(source)
            X = np.array(X.sum(axis=0).flatten().T).squeeze()

            y = label_dict[y]
            y = to_categorical(y, num_classes=n_classes)

            batch_features[i] = X
            batch_labels[i] = y
        yield batch_features, batch_labels


def define_model():
    try:
        return load_model('test_model.h5')
    except Exception as e:
        print(e)
    print('defining new model')
    model = Sequential()
    model.add(Dense(128, input_shape=(vector_len,)))
    model.add(Activation('relu'))
    Dropout(.3)

    model.add(Dense(
        n_classes,))
    model.add(Activation('softmax'))

    return model


model = define_model()

print('starting')


def top_k_categorical_accuracy(y_true, y_pred, k=4):
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), k))


checkpointer = ModelCheckpoint(filepath='test_model.h5', verbose=1, save_best_only=False)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=[top_k_categorical_accuracy])
history = model.fit_generator(
    generator(),
    epochs=10,
    verbose=1,
    steps_per_epoch=10,
    use_multiprocessing=True,
    callbacks=[checkpointer])

model.save('test_model.h5')
