import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from vectorizer_nn import vectorize_article
from keras.models import load_model
from itertools import islice
import numpy as np
from keras.utils.np_utils import to_categorical
from keras.metrics import top_k_categorical_accuracy

articles = vectorize_article()

n_classes = 17

labels = [
    'extreme left', 'right', 'mixed', 'very high', 'right-center', 'left', 'propaganda', 'satire',
    'extreme right', 'pro-science', 'hate', 'left-center', 'fake news', 'high', 'center', 'low',
    'conspiracy'
]

label_dict = {k: i for i, k in enumerate(labels)}


class X_shape:
    shape = None


vector_len = 15000


def generator():
    print('vectorized article')
    source = articles
    print('produced source')
    labels = dict()

    batch_size = 10
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
    model.add(Dense(64, input_shape=(vector_len,)))
    model.add(Activation('sigmoid'))
    Dropout(.3)

    model.add(Dense(
        n_classes,))
    model.add(Activation('softmax'))

    return model


model = define_model()

# In[371]:

# from sklearn.model_selection import train_test_split

# x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.15)
# In[ ]:
print('starting')

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['top_k_categorical_accuracy'])
history = model.fit_generator(generator(), epochs=20, verbose=1, steps_per_epoch=210)
# score = model.evaluate(x_test, y_test, batch_size=30, verbose=1)
model.save('test_model.h5')
