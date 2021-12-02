import random

import nltk
from nltk.corpus import semcor, stopwords
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Lemma
from nltk.stem import WordNetLemmatizer

LEMMATIZER = WordNetLemmatizer()
STOPWORDS = stopwords.words("english")


def sentence_to_bag_of_words(sent):
    return {
        LEMMATIZER.lemmatize(word).lower()
        for word in sent
        if word.isalnum()
        and word.lower() not in STOPWORDS
    }


def synset_to_bag_of_words(sense):
    signature = sentence_to_bag_of_words(sense.definition())

    for example in sense.examples():
        signature |= sentence_to_bag_of_words(example)

    return signature


def find_best_sense(word):
    return wn.synsets(word)[0]


def lesk(word, sentence):
    best_sense = find_best_sense(word)
    max_overlap = 0
    context = sentence_to_bag_of_words(sentence)

    for sense in wn.synsets(word):
        signature = synset_to_bag_of_words(sense)
        overlap = len(signature & context)

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense


# Valutazione


def is_lemma(o):
    return isinstance(o, nltk.tree.Tree) and isinstance(o.label(), Lemma)


def is_noun(w):
    return w.label().synset().pos() == "n"


def is_polysemic(w):
    return len(wn.synsets(w.label().name())) > 1


def remove_tags(sent):
    return [l.label().name() if is_lemma(l) else l[0] for l in sent]


def pick_a_random_noun(sent):
    nouns = [
        word.label()
        for word in sent
        if is_lemma(word) and is_noun(word) and is_polysemic(word)
    ]

    if nouns:
        return random.choice(nouns)


def random_words_sentences(tagged_corpus, n=50):
    sentences_and_targets = []

    for sentence in random.choices(tagged_corpus, k=n):
        target = pick_a_random_noun(sentence)

        if target is not None:
            sentences_and_targets.append(
                (
                    sentence_to_bag_of_words(remove_tags(sentence)),
                    target,
                )
            )

    if len(sentences_and_targets) < n:
        sentences_and_targets.extend(
            random_words_sentences(
                tagged_corpus, n - len(sentences_and_targets)
            )
        )

    return sentences_and_targets


def accuracy(results):
    corrects = 0

    for result, target in results:
        if target.synset() == result:
            corrects += 1

    return corrects / len(results)


def wsd(n):
    accuracies = []

    for i in range(n):
        words_sentences = random_words_sentences(
            semcor.tagged_sents(tag="sem")
        )
        results = [
            (lesk(target.name(), sentence), target)
            for sentence, target in words_sentences
        ]
        accuracies.append(accuracy(results))
        print(f"Round {i+1}: {accuracies[-1]:.2%}")

    mean = sum(accuracies) / len(accuracies)
    print(f"\nMean: {mean:.2%}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        random.seed(sys.argv[1])

    wsd(5)
