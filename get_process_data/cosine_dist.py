from glob import glob
from helpers import timeit
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
import os
import joblib

from helpers import LemmaTokenizer

from models import Model


@timeit
def orchestrate(article):
    return list(Classify(article))


class VectorFit:
    ''' Transform input text to fit the training tf-idf vector '''

    def __init__(self, text_, vec_name, vec):
        self.text = text_

        self.vectorized = vec

    def transform(self):

        text_ = LemmaTokenizer(self.text)
        return self.vectorized.vectorizer.transform(text_)


@timeit
class CosineCalcs:
    ''' input a new vector, recieve all distances back '''

    def __init__(self, in_vect, vec_name, model_vec):
        ''' calculate cosine distance '''
        self.in_vect = in_vect
        self.model_vec = model_vec.nmf
        self.vec_name = vec_name

    def distances(self):

        self.in_vect = self.in_vect.mean(axis=0).reshape(1, -1)

        dist = cosine_distances(self.model_vec, self.in_vect)

        return self.vec_name, round(float(1 - dist), 5)


class Model:

    def __init__(self):
        self.doc_term_matrix = None
        self.vectorizer = None
        self.nmf = None


class Vectors:
    vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}


class Classify:

    def __new__(self, text_input):

        for k, v in Vectors.vectors.items():
            flag = VectorFit(text_input, k, v)
            yield CosineCalcs(flag.transform(), k, v).distances()


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
