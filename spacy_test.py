# Install: pip install spacy && python -m spacy download en
import spacy
import mongo_driver

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en')

# Process a document, of any size
text = open('war_and_peace.txt').read()
doc = nlp(text)

# Hook in your own deep learning models
similarity_model = load_my_neural_network()


def install_similarity(doc):
    doc.user_hooks['similarity'] = similarity_model


nlp.pipeline.append(install_similarity)

doc1 = nlp(u'the fries were gross')
doc2 = nlp(u'worst fries ever')
doc1.similarity(doc2)