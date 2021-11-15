import nltk
from nltk.corpus import semcor
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus.reader.wordnet import Lemma
import random


def is_lemma(o):
    return isinstance(o, nltk.tree.Tree) and isinstance(o.label(), Lemma)


def is_noun(w):
    return w.label().synset().pos() == "n"


def preprocessing(sent):
    porter = PorterStemmer()
    return [porter.stem(word.lower()) for word in sent if word.isalnum()]


def remove_tags(sent):
    return [l.label().name() if is_lemma(l) else l[0] for l in sent]


def get_word_sent(sent):
    nouns = [word.label() for word in sent if is_lemma(word) and is_noun(word)]
    random_noun = random.choice(nouns)
    return random_noun.name(), random_noun, preprocessing(remove_tags(sent))


def random_words_sentences(tagged_corpus):
    # return [get_word_sent(sent) for sent in random.choices(tagged_corpus, k=50)]
    return [get_word_sent(sent) for sent in tagged_corpus[:49]]


def lesk(word, sentence):

    if not wn.synsets(word):
        best_sense = None
    else:
        best_sense = wn.synsets(word)[0]

    max_overlap = set()
    context = set(preprocessing(sentence))

    for sense in wn.synsets(word):
        gloss = {word.lower() for word in sense.definition().split()}
        examples = {word.lower() for example in sense.examples() for word in example.split() if word.isalnum()}
        signature = gloss.union(examples)
        overlap = signature & context

        if len(overlap) > len(max_overlap):
            max_overlap = overlap
            best_sense = sense

    return best_sense


def accuracy(results):
    corrects = 0

    for result, target in results:
        if target in result.lemmas():
            corrects += 1

    return print("accuracy = ", corrects / len(results))


def wsd(n):

    accuracies = []

    for i in range(n):
        words_sentences = random_words_sentences(semcor.tagged_sents(tag="sem"))
        results = [(lesk(word, sentence), target) for word, target, sentence in words_sentences]
        accuracies.append(accuracy(results))

    return 0


if __name__ == "__main__":
    wsd(1)