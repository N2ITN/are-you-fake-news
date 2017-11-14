from newspaper import nlp


def nlp_wrapper(text):
    """Keyword extraction wrapper
    """
    nlp.load_stopwords('en')
    return list(nlp.keywords(text).keys())


if __name__ == '__main__':
    x = '''The site itself is a topic for a post of its own, but in short it uses aws microservices to host machine learning models. When a user enters a new site, 60 or so articles are scraped from the target news site and analyzed for text similarity compared to a corpus of articles using labels from the kind folks at mediabiasfactcheck.com and opensources.co. Charts are then generated reflecting the estimated political bias, accuracy, and other metrics like conspiracy, propaganda and hate. The text similarity algorithm is not 100% and new ideas are still being tested, but it does pick up on the louder signals such as conspiracy or far right. I’m choosing to keep the site low key until I have a refined model in production. Future post incoming because it is an interesting problem with some neat solutions.'''
    print(nlp_wrapper(x))