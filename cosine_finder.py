from glob import glob

import numpy as np
from sklearn.decomposition import NMF
from pprint import pprint
from sklearn.metrics.pairwise import cosine_distances

import joblib
import spacy
from lemmatize_articles import LemmaTokenizer
from NLP_machine import Model

nlp = spacy.load('en_core_web_sm')


def LemmaTokenizer(text_):

    def process():
        tokens = nlp(text_)
        for token in tokens:
            if len(token) > 2 and token.is_alpha and not (
                    token.is_stop):  #and  and token.lemma_ != '-PRON-':
                yield token.lemma_ or token

    return list(process())


class revector:

    def __init__(self, other):
        self.other = other
        self.vectorized = joblib.load('vectorizer.pkl')

    def transform(self):

        text_ = LemmaTokenizer(self.other)
        return self.vectorized.vectorizer.transform([text_])

    def nmf(self):

        dtm = self.transform()
        return NMF(n_components=1).fit(dtm).components_.sum(axis=0).reshape(1, -1)


sample = revector(
    ''' Inert ingredient” is a fickle, deceptive term used on pesticide and herbicide labels to shield severely toxic ingredients from safety testing and consumer scrutiny. “Inert” sounds harmless, but these ingredients fly under the radar untested by U.S. regulatory agencies, and as intended, these inert ingredients make “active” ingredients more potent.

The “active” ingredient of Roundup herbicide is a carcinogen called glyphosate. This chemical has been extensively studied by international research teams that make up the International Agency for Research on Cancer (IARC), a division of the World Health Organization (WHO). After a yearlong study, IARC concluded in 2015 that glyphosate is “probably carcinogenic to humans.” But the toxicity doesn’t end there.

While glyphosate by itself is carcinogenic to humans and destructive to microbe ecology, the parts that don’t get studied are the “inert” ingredients and how their synergy makes glypohate even more devastating to human health. What role do “inert” ingredients play in disrupting human endocrine systems, cellular processes, and assisting the permeation of toxins across the blood-brain barrier?

“Inert” ingredients are designed to enhance glypohsate’s toxicity as an herbicide. Since glyphosate is also a registered antibiotic, it is inevitably doing great damage to human gut health. Becoming part of the food and water supply, glyphosate and its host of inert ingredients work together and deplete the good bacteria that control much of the human digestive and immune systems.

The inert ingredients of Roundup that often go ignored, are actually powerful adjuvants that make glyphosate more pervasive in the environment, delaying the breakdown and decay of glyphosate, while allowing the carcinogen to more readily penetrate tissues. These “inert” ingredients are making glyphosate more of a nightmare long term. It’s the synergistic chemistry that should trouble consumers the most. Consequentially, we are now being exposed to glyphosate in organic products. Human breast milk passes these toxins on to infants. The U.S. regulatory agencies are not monitoring and testing products for glyphosate toxicity or heavy metal accumulation.

In the U.S., pesticide manufacturers are only required to test the active ingredient by itself and not required to test the full formulation; therefore, the true toxicity of Roundup is beyond fathomable.

Caroline Cox of the Center for Environmental Health and Michael Surgan of the Office of the Attorney General of New York State took it upon themselves to study the synergy of glyphosate and the inert ingredients in Roundup. Their paper, published in the journal Environmental Health Perspectives, found that the entire pesticide formulation induced toxic effects greater than the herbicide’s lone active ingredient. Most concerning is the damage the whole product causes to the genetic information of cells. While glypohsate alone causes cancer, the inert ingredients allow glyphosate to penetrate further, damaging chromosomes and causing DNA mutations. In another study, Roundup as a complete formulation was much more lethal to human placenta cells than glyphosate alone. The formulation inhibited the activity of the enzyme aromatase, which plays an important role in the human endocrine system.

Some of the “inert” ingredients by themselves may actually be more toxic to humans than glypohsate. When studying the toxicity of nine pesticides and their individual ingredients, Caen researcher, Gilles-Eric Seralini found that an adjuvant of glyphosate, polyethoxilated tallowamine, was more deadly than glyphosate when tested on human umbilical, embryonic and placental cells. Eight of the nine formulations were “one thousand times” more toxic than the active ingredients alone.

In conjunction, French scientists concluded that “inert” ingredients in Roundup are 10,000 times more toxic than glyphosate alone. Their study, “Major Pesticides Are More Toxic to Human Cells Than Their Declared Active Principles,” was published in Biomedical Research International in 2014. '''
)

pickle_jar = glob('./lsa_*.pkl')

vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in pickle_jar}


def get_v(name):
    return vectors[name].components_.sum(axis=0).reshape(1, -1)


def get_dist(v1):

    def distances():
        for k in vectors:
            yield k, round(1. - float(cosine_distances(get_v(k), v1)), 3)

    return sorted(list(distances()), key=lambda _: _[1], reverse=True)


def cosine():
    done = set()
    for k in vectors:
        done.add(k)
        for k1 in vectors:
            if not k1 in done:
                done.add(k1)
            else:
                continue

            yield ' : '.join(sorted((k, k1))), round(1. - float(cosine_distances(get_v(k), get_v(k1))),
                                                     3)

    cosine_dist_dict = {k: v for k, v in cosine()}
    sorted(cosine_dist_dict.items(), key=lambda kv: kv[1], reverse=True)


if __name__ == '__main__':
    pprint(get_dist(sample.nmf()))
