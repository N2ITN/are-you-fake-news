from itertools import islice
import os
from tensorflow import keras
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np

Sequential = keras.models.Sequential
load_model = keras.models.load_model
Tokenizer = keras.preprocessing.text.Tokenizer
Activation = keras.layers.Activation
Dense = keras.layers.Dense
Dropout = keras.layers.Dropout
SGD = keras.optimizers.SGD
K = keras.backend
BatchNormalization = keras.layers.BatchNormalization
top_k_categorical_accuracy = keras.metrics.top_k_categorical_accuracy
to_categorical = keras.utils.to_categorical
ModelCheckpoint = keras.callbacks.ModelCheckpoint

from vectorizer_nn import vectorize_article, n_articles
labels = [
    'center', 'conspiracy', 'extreme left', 'extreme right', 'fake news', 'hate', 'high', 'left',
    'left-center', 'low', 'mixed', 'pro-science', 'propaganda', 'right', 'right-center', 'satire',
    'very high'
]

n_classes = len(labels)

label_dict = {k: i for i, k in enumerate(labels)}

vector_len = 20000

articles = vectorize_article()


def encoder(flags):
    return np.array([1 if _ in flags else 0 for _ in labels])


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

            y = encoder(y)
            # y = to_categorical(y, num_classes=n_classes)

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
    model.add(Dense(256, input_shape=(vector_len,)))
    model.add(Activation('relu'))
    model.add(BatchNormalization())
    model.add(Dense(
        n_classes,))
    model.add(Activation('sigmoid'))

    return model


model = define_model()

print('starting training')


def top_k_categorical_accuracy(y_true, y_pred, k=3):
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), k))


def train():
    # sgd = SGD(nesterov=True, momentum=0.8)
    checkpointer = ModelCheckpoint(filepath='test_model.h5', verbose=1, save_best_only=False)
    model.compile(loss='binary_crossentropy', optimizer='nadam', metrics=['accuracy'])
    history = model.fit_generator(
        generator(),
        epochs=10,
        verbose=1,
        max_queue_size=100,
        workers=8,
        steps_per_epoch=n_articles / 10 // (64 + 1),
        use_multiprocessing=True,
        callbacks=[checkpointer])

    model.save('test_model.h5')


if __name__ == '__main__':
    train()
