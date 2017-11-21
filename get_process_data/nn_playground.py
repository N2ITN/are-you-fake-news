# coding: utf-8

# In[374]:

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from vectorizer_nn import vectorize_article
from keras.models import load_model
from itertools import islice
import numpy as np
from keras.utils.np_utils import to_categorical

# In[363]:

articles = list(islice(vectorize_article(), 4000))

# In[364]:

y, X = list(zip(*articles))

labels = {name: i for i, name in enumerate(set(y))}

X = np.array([_.todense().sum(axis=0).flatten().T for _ in X]).squeeze()

y = [labels[n] for n in y]
n_classes = len(set(y))

y = to_categorical(y)

# In[375]:


def define_model():
    try:
        return load_model('test_model.h5')
    except Exception as e:
        print(e)
    model = Sequential()
    model.add(Dense(512, input_shape=(10000,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(
        n_classes,))
    model.add(Activation('softmax'))

    return model


model = define_model()

# In[371]:

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.15)
# In[ ]:

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(x_train, y_train, batch_size=30, epochs=10, verbose=1, validation_split=0.1)
score = model.evaluate(x_test, y_test, batch_size=30, verbose=1)
model.save('test_model.h5')
