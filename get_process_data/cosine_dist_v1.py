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
        components = CosineCalcs.vectors[vname] * 100000

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
    '''Imagine if you found out from your doctor that you had breast cancer, or that your child developed autism after the pediatrician administered too many chemical medications too close together. What if, immediately after you asked him a few important questions, he ran to his computer and bad-mouthed you in an incessant rant for thousands of readers to see? Consider this carefully.

“It is a serious matter when a medical doctor abuses the trusted status of a licensed medical professional to abuse, bully, disparage, and attack others. It is worse when he uses that status and trusted position to lie about published medical research to make false claims intended to mislead and actively spread deliberate misinformation about medical knowledge whilst doing so to make false claims about others.  It is even worse when he does it so publicly and routinely, publishing to mislead people worldwide and on a daily basis on the internet.” This quote comes from Child Health Safety blog published on November 2, 2014 in regards to David H. Gorski, an elusive and secretive internet troll.

The following two quacks are chemical violence promoters and self-admitted pharma shills who often source themselves and cite their own fabricated studies, including highly-opinionated blogs as “credible” sources. They are both also guilty of regurgitating industry propaganda in medical “definitions” found on Wikipedia. They both use online media to create “entries” that attempt to defame and discredit honest journalists, forthright scientists, natural food enthusiasts and holistic medicine practitioners.
Insidious Pharma Shill #1: Dr. Paul Offit, a.k.a. “Skeptical Raptor” – chemical violence promoter and quack pediatrician

It is said that after years of being a criminal or a liar, that crime seems “normal” for the perpetrator and they stop covering their tracks so well. They lose track of all the lies they have told and often leave”bread crumbs” making it easy for investigators. Eventually, they are caught, exposed and their “reign of terror” comes to an end.

If you Google it, you can easily discover that Paul Offit, a.k.a. Skeptical Raptor, admits that he has “co-authored a couple of articles on Wikipedia” and wrote “… articles on skepticism and debunking pseudoscience … .” This is no surprise to investigative journalists who also know that Wikipedia was founded by a Porn King (“Bomis” Jimmy Wales) using monies from running porno sites for men. Even school children know better than to use Wikipedia when seeking factual information for research or reports.

Offit’s cohorts recently slipped up in emails where they quoted a Medscape article that Offit wrote under his alias “Skeptical Raptor” (see page 8 of this PDF file).

Offit’s “partner in crime” also sends him an email that states in the subject line a “call for action by Skeptical Raptor” (on page 53 of the PDF) , and also in the anchor text of the url it reads another ominous call to action, reading “time-regulate-antivaccine-liars-existence…” – which almost sounds like some kind of violent uprising. Then Offit sends back a “thank you” in the corresponding email response.
“Offit the Raptor” promotes injecting children with deadly pig virus-laden vaccine he invented, patented, and profited from by the millions

You may be wondering just how much of a sinister scoundrel Dr. Skeptical Raptor can be, so let’s have a look. Imagine if an evil scientist put a few parts per million of poisonous snake venom in a childhood vaccine, patented it, was paid millions of dollars by the corrupt vaccine industry, and the vaccine was promoted by the CDC on their “recommended schedule” of vaccines. Well, the insidious Dr. Paul Offit invented a vaccine (RotaTeq) that contains two strains of a deadly pig virus called circovirus — a virus responsible for killing millions of piglets in China. Circovirus has absolutely NOTHING at all to do with helping children fight off Rotavirus, which is a rather mild flu-like infection that causes diarrhea. Here’s a quote directly from Merck’s vaccine product page:

Parts of porcine circovirus (a virus that infects pigs) types 1 and 2 have been found in RotaTeq.

Could this deadly vaccine be the cause of the massive US outbreak of circovirus, also known as PEDV – porcine epidemic diarrhea virus (or PV-777)? Since Rotavirus causes diarrhea in children, who would ever suspect that the RotaTeq vaccine is the actual cause? Paul Offit covers all of this up with propaganda on the web. In January of 2012, America’s pork industry was devastated by a massive outbreak of porcine diarrhea. The medical industry claims the disease is not transferable to humans, but what about when you inject two strains of it into muscle tissue through a syringe?

Nearly all piglets that get the disease die of it, so what about children injected with it? Could this be why America is experiencing a massive spike in autism, and why the vaccine industry has paid out $3 billion in compensation to vaccine-injured families?

The Skeptical Raptor Paul Offit is a dominating moderator on Wikipedia and describes himself as a pharma shill (which means you’re paid to lie). He says it’s safe to eat MSG and high fructose corn syrup (HFCS), and that health nuts are going way overboard worrying about them. He also promotes Monsanto’s deadly DDT pesticide, making a fool of himself and leaving a trail of nonsense strewn across the internet.

One of Offit’s heroes is Dr. Maurice Hilleman, a renowned Merck vaccine scientist who admitted to major fraud in the field of vaccine research. Vaccine developer Dr. Hilleman mentored Offit at the Children’s Hospital of Philadelphia. Dr. Hilleman has gone on record (decades ago) admitting the presence of SV40 (cancer as leukemia) and AIDS viruses in vaccines that were administered to millions of Americans. When asked why this didn’t get out to the press, he replied: “Obviously you don’t go out, this is a scientific affair within the scientific community.” In other words, vaccine scientists cover for other vaccine scientists and keep all their dirty secrets within their own circle, covering up the contamination of their vaccines.
Insidious Pharma Shill #2: David H. Gorski, a.k.a. “Orac” – the most abusive blogger still practicing quack medicine today

Meet “Orac” (also found under pseudo-name “Respectful Insolence”) – the blogging psycho freak surgeon (real name David H. Gorski) who blogs before, after, and possibly during operations on women’s breasts, so he can bad mouth anyone who questions the safety of experimental, dangerous chemical-laden medicine like chemotherapy and vaccines. Gorski works under the same company umbrella (Karmanos Cancer Center) as the infamous Farid Fata, who is serving 45 years in federal prison for defrauding Medicare (for millions of dollars) and dosing thousands of healthy patients with concentrated chemotherapy drugs, even killing several hundred of them.

Gorski hides behind his mask during surgery and after, when he blogs under his pseudo-name Orac – that he stole from an old British science fiction television show. He writes over 20,000 words in each blog, trolling the internet and defaming anyone that opposes chemical medicine, yet none of his patients know this. Gorski even encourages his followers to create fake emails and fake identities and abuse families on medical message boards who post complaints and injuries from vaccines, chemotherapy or pharmaceuticals.

So now the one all-important question must be answered: Is David H. Gorski as insane as his imprisoned colleague Dr. Farid Fata? You be the judge. Gorski has an alter-ego (think Jekyll and Hyde here) that surfaces in his rants on blogs across the internet and at his “quack buster” seminars. Here are just a few of the various insane posts Orac has written. What would you do if you found out this was YOUR doctor?

Orac’s direct words from Nov 11, 2015 as posted on “Scienceblogs.com”… (which is now shutting down after being wholly discredited)

“I’m a pretty piss-poor pharma whore.”

“I’m a Pharma Funded Shill, supported by National Geographic.”

“I love the persona of Orac and being known by the name of a supercomputer featured on an obscure (in this country) British science fiction show popular over 30 years ago.”

“You know, at this point, I’m tempted to stand up, puff out my chest, put on my bravest, most serious face, and declare,“I am Spartacus!”

Gorski has a very long history of character assassinating holistic doctors. Here’s a quote where he calls himself out, saying he uses “public character assassination to entertain the skeptic community.”

April, 2012: Gorski trolls the internet, impersonating disease-injured families on comment boards:

Use emotional warfare on anti-vax blogs. Tell emotional stories full of tears and sobbing and unbearable grief and terror, about people in your own family or people you read about, who were sick with or died of terrible diseases. Don’t hold back details about bodily fluids and suchlike: the more gross the better. This stuff has a way of infiltrating the minds of readers and subtly influencing their decisions, in a manner similar to advertising.

Go in there and “agree with them” and then say things that appear thoroughly delusional, overtly nuts, blatantly and obviously wrong even to nincompoops, etc. Occasional spelling and grammar errors are also useful but don’t over-do. The point of this exercise is to create an impression that drives away undecideds who may come in to check out these sites. It helps to do this as a group effort and begin gradually, so the sites appear to be “going downhill slowly.

But it is useful to have an email address that can’t be traced back, for certain legitimate and ethical uses, just as it is useful to have a mail box at say the UPS store. 

… The way to fight it is by sabotaging the anti-vaxers with crazy stuff that drives away undecideds. The way to fight it is with emotional narratives that undermine the ones that the anti-vaxers are pushing.

At one point, Orac wrote this on his own blog, describing himself:

Yes, in the case of a true ‘shill’ who does not reveal that he works for a pharmaceutical company and pretends to be ‘objective’

Gorski also blogs and pretends to be a woman named “SoCalGal”

Also, refer to “Unmasking ORAC”

This has been a public service announcement to help Americans avoid psychotic doctors.''')

print(x)
