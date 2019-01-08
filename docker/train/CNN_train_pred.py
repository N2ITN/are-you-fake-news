# coding: utf-8
#%%
from pprint import pprint

from tensorflow import keras
import numpy as np
import pickle
import json
from unidecode import unidecode_expect_nonascii, unidecode


class Corpus:
    ''' Retrieves data from MongoDB'''

    def __init__(self, db_table='articles', field='title', n_words=20000):

        self.n_words = n_words
        self.field = field
        self.db_table = db_table
        self.labels = [
            'center', 'conspiracy', 'extreme left', 'extreme right', 'fake news', 'hate', 'high', 'left',
            'left-center', 'low', 'mixed', 'pro-science', 'propaganda', 'right', 'right-center',
            'satire', 'very high'
        ]

    def get_all_rows(self):
        from pymongo import MongoClient
        client = MongoClient(connect=False)
        db = client['newscraper']
        ''' Retrieve target table from db '''
        print(self.n_words)
        self.articles = [_ for _ in db[self.db_table].find() if _[self.field]]
        self.n_articles = len(self.articles)


class KerasVectorizer(Corpus):
    ''' Performs vectorization and text preprocessing '''

    def __init__(self, dnn_type='seq', max_len=1000, predict_str=False):
        super().__init__()
        if not predict_str:
            self.get_all_rows()
            self.train = True
        else:
            self.articles = predict_str
            self.train = False
        self.dnn_type = dnn_type
        self.max_len = max_len

    def clean(self, seq):
        if len(seq):
            seq = unidecode(seq)
            return ' '.join(
                keras.preprocessing.text.text_to_word_sequence(
                    seq, filters='''1234567890!"#$%&()*+,-\n./—:;<=>?@[\\]^_`{|}~\t\'“”'''))

    def fit(self):
        ''' Fit vectorizer on corpus '''

        Tokenizer = keras.preprocessing.text.Tokenizer
        tokenizer = Tokenizer(self.n_words)

        print('cleaning text')
        texts = [self.clean(entry[self.field]) for entry in self.articles]
        print('fitting vector')
        tokenizer.fit_on_texts(texts)
        pickle.dump(tokenizer, open('vector.pkl', 'wb'))
        self.corpus_vector = tokenizer
        self.lookup = {k: v for k, v in self.corpus_vector.word_index.items() if v < self.n_words}

        json.dump(self.lookup, open('lookup.json', 'w'))

    def gen_x_onehot(self):
        if self.train:
            text = [self.clean(_[self.field]) for _ in self.articles]
        else:
            text = self.articles
        for entry in text:
            entry = keras.preprocessing.text.text_to_word_sequence(entry)
            yield [self.lookup[word] for word in entry if word in self.lookup]

    def transform_x_onehot(self):
        x = list(self.gen_x_onehot())

        self.rev_lookup = {v: k for k, v in self.lookup.items()}
        v_len = self.max_len
        print('using limit of', v_len)
        self.lens = []
        for entry in x:
            self.lens.append(len(entry))

            if len(entry) >= v_len:
                yield np.array(entry[-v_len:])
            else:
                yield np.array([0 for _ in range(v_len - len(entry))] + entry)

    def transform_y(self):
        ''' Vectorizes y labels '''
        for entry in self.articles:
            yield np.array([1 if _ in entry['flags'] else 0 for _ in self.labels])

    def transform_x(self):
        ''' Transforms texts to the vector '''
        vector = pickle.load(open('./_nlp_lambda/code/vector.pkl', 'rb'))

        self.lookup = json.load(open('./_nlp_lambda/code/lookup.json'))

        return list(self.transform_x_onehot())

    def x_y(self):
        self.fit()
        print('producing x, y data')
        y = list(self.transform_y())

        if self.dnn_type == 'seq':
            x = list(self.transform_x_onehot())
        elif self.dnn_type == 'bow':
            x = self.transform_x()
        return x, y


def prep_data():
    k_v = KerasVectorizer(max_len=1000)
    #http://www.newswhip.com/2013/12/article-length/
    x, y = k_v.x_y()
    print('data prepared')
    # print(x[0].shape)

    return k_v, x, y


def predict_data(text):
    k_v = KerasVectorizer(max_len=1000, predict_str=[text])

    x = k_v.transform_x()
    # print('data prepared')
    # print(x[0].shape)

    return k_v, x


text = '''Prime Minister Thatcher once famously observed that socialists “always run out of other people’s money.” But what actually happens when socialism runs out of money?

(Article by Daniel Greenfield republished from FrontpageMag.com)

Venezuela, a once wealthy nation with black gold coming out of the ground, is a test case.
'''

len(text.split())

k_vp, xp = predict_data(text)

# print(xp[0])


def train_setup():

    def val_set(x, y):
        val_size = .15
        val_ind = int(len(x) * val_size)
        print(val_ind, len(x))

        randomize = np.arange(len(x))
        np.random.shuffle(randomize)

        x = np.array(x)[randomize]
        y = np.array(y)[randomize]

        x = x[:-val_ind]
        y = y[:-val_ind]
        x_val = x[-val_ind:]
        y_val = y[-val_ind:]
        assert len(y) == len(x)

        return x, y, x_val, y_val

    k_v, X, Y = prep_data()
    x, y, x_val, y_val = val_set(X, Y)


def dnn():

    Sequential = keras.models.Sequential
    load_model = keras.models.load_model
    Tokenizer = keras.preprocessing.text.Tokenizer
    Activation = keras.layers.Activation
    SGD = keras.optimizers.SGD
    Adam = keras.optimizers.Adam
    BatchNormalization = keras.layers.BatchNormalization
    to_categorical = keras.utils.to_categorical
    ModelCheckpoint = keras.callbacks.ModelCheckpoint
    Embedding = keras.layers.Embedding
    Reshape = keras.layers.Reshape
    Flatten = keras.layers.Flatten
    Dropout = keras.layers.Dropout
    Concatenate = keras.layers.Concatenate
    Dense = keras.layers.Dense
    Model = keras.models.Model
    Input = keras.layers.Input
    Conv2D = keras.layers.Conv2D
    MaxPool2D = keras.layers.MaxPool2D

    n_classes = 17

    def define_model_rnn():
        vector_len = x[0].shape[0]
        vocab_size = k_v.n_words
        embedding_dim = 10
        model = Sequential()
        model.add(keras.layers.Embedding(vocab_size, embedding_dim, input_shape=(vector_len,)))
        model.add(keras.layers.GRU(3, dropout=0.2, recurrent_dropout=0.2))
        model.add(Activation('relu'))
        model.add(Dense(
            n_classes,))
        model.add(Activation('sigmoid'))
        return model

    def define_model():
        vector_len = k_v.n_words
        model = Sequential()
        model.add(Dense(128, input_shape=(vector_len,)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dense(32))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(Dense(
            n_classes,))
        model.add(Activation('sigmoid'))
        return model

    def define_model_cnn():

        sequence_length = x.shape[1]
        vocabulary_size = k_v.n_words
        embedding_dim = 5
        filter_sizes = [3, 4, 5]
        num_filters = 512
        drop = 0.5

        epochs = 100
        batch_size = 30

        inputs = Input(shape=(sequence_length,), dtype='int32')
        embedding = Embedding(
            input_dim=vocabulary_size, output_dim=embedding_dim, input_length=sequence_length)(inputs)
        reshape = Reshape((sequence_length, embedding_dim, 1))(embedding)

        conv_0 = Conv2D(
            num_filters,
            kernel_size=(filter_sizes[0], embedding_dim),
            padding='valid',
            kernel_initializer='normal',
            activation='relu')(reshape)
        conv_1 = Conv2D(
            num_filters,
            kernel_size=(filter_sizes[1], embedding_dim),
            padding='valid',
            kernel_initializer='normal',
            activation='relu')(reshape)
        conv_2 = Conv2D(
            num_filters,
            kernel_size=(filter_sizes[2], embedding_dim),
            padding='valid',
            kernel_initializer='normal',
            activation='relu')(reshape)

        maxpool_0 = MaxPool2D(
            pool_size=(sequence_length - filter_sizes[0] + 1, 1), strides=(1, 1),
            padding='valid')(conv_0)
        maxpool_1 = MaxPool2D(
            pool_size=(sequence_length - filter_sizes[1] + 1, 1), strides=(1, 1),
            padding='valid')(conv_1)
        maxpool_2 = MaxPool2D(
            pool_size=(sequence_length - filter_sizes[2] + 1, 1), strides=(1, 1),
            padding='valid')(conv_2)

        concatenated_tensor = Concatenate(axis=1)([maxpool_0, maxpool_1, maxpool_2])
        flatten = Flatten()(concatenated_tensor)
        dropout = Dropout(drop)(flatten)
        output = Dense(units=n_classes, activation='sigmoid')(dropout)
        model = Model(inputs=inputs, outputs=output)
        return model

    label_dict = {k: i for i, k in enumerate(k_v.labels)}

    print('starting training')

    def train():
        model = define_model_cnn()
        lr1 = Adam(lr=0.00005)
        lr2 = Adam(lr=0.0001)
        adam = Adam(lr=0.001)
        early_stop = keras.callbacks.EarlyStopping(
            monitor='val_loss', min_delta=0, patience=5, verbose=1, mode='auto')
        #         checkpointer = ModelCheckpoint(filepath='CNN20k.h5', verbose=1, save_best_only=False)
        model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
        history = model.fit(
            np.array(x),
            np.array(y),
            epochs=1000,
            verbose=1,
            validation_data=(x_val, y_val),
            callbacks=[
                keras.callbacks.TensorBoard(
                    log_dir='./logs/article_clean_20k_CNN_5d_SAVED', write_graph=False), early_stop,
                checkpointer
            ])

    train()


# dnn()

load_model = keras.models.load_model
model = load_model('./_nlp_lambda/code/CNN20k.h5')

label_dict = {i: k for i, k in enumerate(k_vp.labels)}

preds = [model.predict(np.array(text).reshape(1, -1)) for text in xp]
np.set_printoptions(precision=5, suppress=True)
pred_dict = {label_dict[i]: '{0:.6f}'.format(p) for i, p in enumerate([_ for _ in preds[0].flatten()])}

final_output = [{label_dict[i]: round(float(p), 6) for i, p in enumerate([_ for _ in pred.flatten()])}
                for pred in preds]

pprint(sorted(pred_dict.items(), key=lambda kv: kv[1], reverse=True))

import pandas as pd
#%matplotlib inline

res = pd.DataFrame(final_output).transpose()#.reset_index()
res.columns = ['rating']
res.sort_values('rating').plot(kind='barh')
#%%

# from itertools import islice
# rank = (_ for _ in k_v.rev_lookup.items())
# [next(rank) for _ in range(18999)]
# pprint([next(rank) for _ in range(1000)])
