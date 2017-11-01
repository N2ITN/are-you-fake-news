from glob import glob
from helpers import timeit
import numpy as np
from sklearn.metrics.pairwise import cosine_distances

import joblib

from helpers import LemmaTokenizer

from models import Model


@timeit
def orchestrate(article):
    return Classify(article)


class VectorFit:
    ''' Transform input text to fit the training tf-idf vector '''

    def __init__(self, other):
        self.other = other

        self.vectorized = joblib.load('vectorizer.pkl')

    def transform(self):

        text_ = LemmaTokenizer(self.other)
        return self.vectorized.vectorizer.transform(text_)


@timeit
class CosineCalcs:
    ''' input a new vector, recieve all distances back '''
    vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}

    def __init__(self, vec):
        ''' calculate cosine distance '''
        self.in_vect = vec

    def vec_from_model(self, vname):
        components = CosineCalcs.vectors[vname].components_
        # print(components.shape)
        # print(components.mean(axis=0).shape)
        return components.mean(axis=0).reshape(1, -1)
        # array = components[0]
        # for row in components[1:]:
        #     array += np.square(row)

        # return array.reshape(1, -1)

    def distances(self):
        for v in CosineCalcs.vectors:
            # print(self.in_vect.shape)
            # print(self.in_vect.mean(axis=0).shape)
            # print(self.vec_from_model(v).shape)
            # print('wtf')
            # exit()

            dist = cosine_distances(self.vec_from_model(v), self.in_vect.mean(axis=0)).T
            # print(dist.shape)
            yield v, round(float(1 - dist), 3)
            # yield v, round(1. - float(cosine_distances(self.vec_from_model(v), self.in_vect)), 3) 


class Model:

    def __init__(self):
        self.doc_term_matrix = None
        self.feature_names = None
        self.flag_index = []
        self.vectorizer = None


class Classify:

    def __new__(self, text_input):

        return Classify.classify_text(text_input)

    @timeit
    def classify_text(input_str):

        sample = VectorFit(input_str)

        try:
            return list(CosineCalcs(sample.transform()).distances())
        except ValueError as e:
            print(e)
            return {}


if __name__ == '__main__':
    print(
        orchestrate(('''Call it how it is
    Hendrix
    I promise, I swear, I swear
    You heard, spit it, yo

    Percocets, molly, Percocets
    Percocets, molly, Percocets
    Rep the set, gotta rep the set
    Chase a check, never chase a bitch
    Mask on, fuck it, mask off
    Mask on, fuck it, mask off
    Percocets, molly, Percocets
    Chase a check, never chase a bitch
    Don't chase no bitches

    Two cups, toast up with the gang
    From food stamps to a whole 'nother domain
    Out the bottom, I'm the livin' proof (Super)
    Ain't compromising, half a million on the coupe
    Drug houses, lookin' like Peru
    Graduated, I was overdue
    Pink molly, I can barely move
    Ask about me, I'm gon' bust a move
    Rick James, thirty-three chains
    Ocean air, cruisin' Biscayne
    Top off, that’s a liability
    Hit the gas, boostin' my adrenaline

    Percocets, molly, Percocets
    Percocets, molly, Percocets
    Rep the set, gotta rep the set
    Chase a check, never chase a bitch
    Mask on, fuck it, mask off
    Mask on, fuck it, mask off
    Percocets, molly, Percocets
    Chase a check, never chase a bitch
    Don't chase no bitches

    [Verse 2]
    Four-door Maybach, I drive anything
    Buy my Range, make 'em go insane
    (Oh my Lord, praise him be)
    My guillotine, drank promethazine
    TEC and beams, go to those extremes
    Parliament, calamari Wednesday
    Parlay in Vegas, we was in attendance
    Before the business, Theodore lenses
    Theo-Dur prescriptions, focus on the missions
    Intermission, never take a break
    Switch states, touch down, foreign plates
    Ain't no way, ain't no fuckin' way
    We call the play, we didn't come to play
    Rob the bank, we gon' rob the game
    They gang, we gang
    But they are not the same (Freebandz)


    [Chorus]
    Percocets, molly, Percocets
    Percocets, molly, Percocets
    Rep the set, gotta rep the set
    Chase a check, never chase a bitch
    Mask on, fuck it, mask off
    Mask on, fuck it, mask off
    Percocets, molly, Percocets
    Chase a check, never chase a bitch
    Don't chase no bitches

    [Outro]
    Mask on, fuck it, mask off
    Mask on, fuck it, mask off
    Mask on, fuck it, mask off
    Gas gone, never nod off
    (Cold chills, prison cells)
    (Oh my Lord, praise him be)

    ''')))
