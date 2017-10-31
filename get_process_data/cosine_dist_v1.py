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

        self.vectorized = joblib.load('./vectorizer.pkl')

    def transform(self):

        text_ = LemmaTokenizer(self.other)
        print(text_)
        return self.vectorized.vectorizer.transform(text_)


@timeit
class CosineCalcs:
    ''' input a new vector, recieve all distances back '''
    vectors = {f.replace('./lsa_', '').replace('.pkl', ''): joblib.load(f) for f in glob('./lsa_*.pkl')}

    def __init__(self, vec):
        ''' calculate cosine distance '''
        self.in_vect = vec.mean(axis=0)
        print(dir(vec))
        print(vec.get_shape())

    def vec_from_model(self, vname):
        components = CosineCalcs.vectors[vname]

        return np.squeeze(components).reshape(1, -1)

    #     array = components[0]
    #     for row in components[1:]:
    #         array += np.square(row)

    # return array.reshape(1, -1)

    def distances(self):
        for v in CosineCalcs.vectors:
            yield v, float(cosine_distances(self.vec_from_model(v), self.in_vect).T[0])


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


x = orchestrate(
    '''A judge says she has the authority to countermand the Commander in Chief’s July decision to reject transgender applicants for military service, highlighting the judiciary’s continued efforts to seize political power from legislators and President Donald Trump.

The claim was made October 30, when Judge Colleen Kollar-Kotelly on the United States District Court for the District of Columbia denounced Trump’s ‘Presidential Memorandum’ ending President Barack Obama’s policy of recruiting people who think they are members of the opposite sex.

She insisted that Trump’s policy be blocked pending a full trial:

    The Court will preliminarily enjoin Defendants from enforcing the following directives of the [Trump] Presidential Memorandum, referred to by the Court as the Accession and Retention Directives:

    I am directing the Secretary of Defense, and the Secretary of Homeland Security with respect to the U.S. Coast Guard, to return to the longstanding policy and practice on military service by transgender individuals that was in place prior to June 2016 until such time as a sufficient basis exists upon which to conclude that terminating that policy and practice would not have the negative effects discussed above.

The judge ordered the Pentagon to continue Obama’s policy of recruiting people who think they are members of the opposite sex, pending a trial and a final decision. The Democratic-nominated judge also insisted that the Trump’s policy would hurt the military, declaring that:

    On the record before the Court, there is absolutely no support for the claim that the ongoing service of transgender people would have any negative effective on the military at all. In fact, there is considerable evidence that it is the discharge and banning of such individuals that would have such effects.

The lawsuit was brought by progressive groups, including the National Center for Lesbian Rights, after Trump reversed Obama’s pro-transgender policies, even though Obama has admitted twice that those policies helped Trump get elected.

Obama’s Pentagon transgender policy reached far beyond military readiness because it marked federal support for the core ideological demand made by transgender activists — that the government must compel Americans to treat a man as a woman (or vice versa) if he says he has an opposite-sex “gender identity,” even if the man has not taken any female hormones or undergone genital cosmetic surgery.

The judge endorsed this dramatic “gender identity” ideological claim, saying:

    The Court holds that Plaintiffs are likely to succeed on their Fifth Amendment claim. As a form of government action that classifies people based on their gender identity, and disfavors a class of historically persecuted and politically powerless individuals, the President’s directives are subject to a fairly searching form of scrutiny. Plaintiffs claim that the President’s directives cannot survive such scrutiny because they are not genuinely based on legitimate concerns regarding military effectiveness or budget constraints, but are instead driven by a desire to express disapproval of transgender people generally. The Court finds that a number of factors— including the sheer breadth of the exclusion ordered by the directives, the unusual circumstances surrounding the President’s announcement of them, the fact that the reasons given for them do not appear to be supported by any facts, and the recent rejection of those reasons by the military itself—strongly suggest that Plaintiffs’ Fifth Amendment claim is meritorious.

    Grateful for such a clear, powerful ruling for our plaintiffs: no legitimate reason to treat #transgender service members differently. https://t.co/vfl3HMe50B

    — Shannon Minter (@shannonminter5) October 30, 2017

When implemented in the military, the transgender ideology forces female soldiers to give “dignity and respect” to transsexual men who join them in their shared shower rooms, according to Obama-era training manuals leaked by soldiers in a mandatory class. But this “dignity and respect” is a one-way street, according to the training slides, which were developed by officials working for former President Barack Obama. “Transgender Soldiers are not required or expected to modify or adjust their behavior based on the fact that they do not ‘match’ other Soldiers,” according to the slides, which were first leaked by TheFederalist.com.

In general, transgender activists want the federal government to wipe out the different, overlapping and complementary civic expectations for men and women in a two-sex society. These expectations include sexual privacy in single-sex showers, matched competition in male or female sports leagues, psychological reassurance in women’s shelters, as well as distinct male and female ideals for appearance and accomplishment.

In contrast, the activists seek a “gender-free” society where the government suppresses any legal, civic or social distinctions between men and women, girls and boys, no matter how popular or beneficial. For example, progressives lauded masculine Olympian Bruce Jenner as an ideal of female beauty when he dressed as a stereotypical pinup model, complete with male genitalia:
transgender

This photo taken by Annie Leibovitz exclusively for Vanity Fair shows the cover of the magazine’s July 2015 issue featuring Bruce Jenner debuting as a transgender woman named Caitlyn Jenner. (Annie Leibovitz/Vanity Fair via AP)

The progressive push to bend Americans’ attitudes and their two-sex civic society around the idea of flexible “gender” has already attacked and cracked popular social practices. For example, the gender claims have shifted rules or practices about different-sex bathrooms, shelters for battered women, sports leagues for girls, hiking groups for boys, K-12 curricula, university speech codes, religious freedoms, free speech, the social status of women, parents’ rights in childrearing, practices to help teenagers, women’s expectations of beauty, culture and civic society, scientific research, prison safety, civic ceremonies, school rules, men’s sense of masculinity, law enforcement, and children’s sexual privacy.

Since Trump’s election, progressive judges have also stepped up their claims that they have the power to redraw election districts and the power to override the president’s authority over who can enter the country. The Supreme Court has not defeated all those power-grabs, partly because the crucial swing-vote judge — Justice Anthony Kennedy — is often sympathetic to progressive social priorities.'''
)

print(x)
