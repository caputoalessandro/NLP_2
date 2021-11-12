import nltk
from nltk.corpus import semcor
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk import tree
import random


def preprocessing(sentences):
    porter = PorterStemmer()
    return [[porter.stem(word) for word in sentence if word.isalnum()] for sentence in sentences]


def lemma_list(sent):
    return [l.label() if isinstance(l, nltk.tree.Tree) else None for l in sent]


def random_words_sentences(corpus, tagged_corpus):
    random_tagged_sents = random.choices(tagged_corpus, k=50)
    tagged_sentences = [lemma_list(sent) for sent in random_tagged_sents]
    return 0


def lesk(word, sentence):

    if not wn.synsets(word):
        best_sense = None
    else:
        best_sense = wn.synsets(word)[0]

    max_overlap = set()
    context = set(sentence)

    for sense in wn.synsets(word):
        gloss = {str(lemma.name()) for lemma in sense.lemmas()}
        examples = {word for example in sense.examples() for word in word_tokenize(example) if word.isalnum()}
        signature = gloss.union(examples)
        overlap = signature & context

        if len(overlap) > len(max_overlap):
            max_overlap = overlap
            best_sense = sense

    return best_sense


def wsd(n):

    results = []

    for i in range(n):
        words_sentences = random_words_sentences(semcor.sents(), semcor.tagged_sents(tag="sem"))
        results.append(lesk(word, sentence) for word, sentence in words_sentences)

    return 0


if __name__ == "__main__":
    wsd(1)