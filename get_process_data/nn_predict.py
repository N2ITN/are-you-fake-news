import keras
import numpy as np
from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential, load_model

from helpers_nlp import transform

vector_len = 15000

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
    model.add(Activation('sigmoid'))

    return model


def orchestrate(text):
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

    pred_dict = {label_dict[i]: p for i, p in enumerate([x for x in preds.flatten()])}

    pretty = sorted(pred_dict.items(), key=lambda kv: kv[1], reverse=True)
    for kv in pretty:
        print(kv)

    return pred_dict


if __name__ == '__main__':
    print(
        orchestrate(
            '''Illegal aliens shielded from deportation under the President Obama-created Deferred Action for Childhood Arrivals (DACA) program are staging a hunger strike in the days leading up to Thanksgiving Day.

The group of illegal aliens from New Jersey have dedicated to not eating until Thanksgiving, according to WNYC, while they lobby Republican members of Congress to pass an amnesty for the nearly 800,000 DACA recipients in the U.S.

“I’m sitting here looking at my last meal and trying to imagine what my meals would be like if I was sent back to Mexico,” DACA illegal alien Adriana Delgado told WNYC.

“People think that I’m crazy for doing this hunger strike but I’m willing to suffer for three days if it means not suffering for a lifetime,” Delgado continued. “There will be thousands of families who will have broken dinner tables if nothing is done.”

The group of illegal aliens is demanding a swift and clean amnesty bill that permanently allows all DACA recipients to remain in the U.S. and puts them on a pathway to U.S. citizenship, where they can eventually bring their foreign relatives to the U.S. as well.

The DACA recipients say they are not satisfied with an amnesty that ties the legalization of potentially 3.3 million eligible illegal aliens to pro-American immigration reforms like an end to chain migration or the termination of the Diversity Visa Lottery.

In September, Attorney General Jeff Sessions announced on behalf of President Trump’s administration that the DACA program would officially be ended in March 2018.

Since the announcement, the Democrat and GOP political establishments have teamed up with the open borders lobby, corporate interests, and the cheap labor industry to push an end-of-the-year amnesty.

An amnesty, though, remains incredibly unpopular with Americans. Most recent polling from Morning Consult and POLITICO revealed that only 23 percent of swing-voters said DACA amnesty should be a “top priority” for Congress, Breitbart News reported.

Overall, fewer than 30 percent of Americans say they support a quick amnesty deal. Even among Democrat voters, amnesty is becoming more and more unpopular, with fewer than 45 percent Democrats wanting Congress to push through an amnesty deal.'''
        ))
