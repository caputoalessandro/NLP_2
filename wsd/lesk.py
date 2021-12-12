from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize


LEMMATIZER = SnowballStemmer('english', ignore_stopwords=True)
STOPWORDS = stopwords.words("english")


def tokens_context(tokens):
    return {
        LEMMATIZER.stem(token).lower()
        for token in tokens
        if token.isalnum()
        and token.lower() not in STOPWORDS
    }


def sentence_context(sent):
    return tokens_context(word_tokenize(sent))


def synset_context(sense: Synset):
    signature = tokens_context([sense.name()])
    signature |= tokens_context(lemma.name() for lemma in sense.lemmas())
    signature |= sentence_context(sense.definition())

    for example in sense.examples():
        signature |= sentence_context(example)

    return signature


def find_best_sense(word):
    return wn.synsets(word)[0]


def lesk(word, tokens):
    best_sense = find_best_sense(word)
    max_overlap = 0
    sentence_ctx = tokens_context(tokens)

    for sense in wn.synsets(word):
        synset_ctx = synset_context(sense)
        overlap = len(sentence_ctx & synset_ctx)

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense
