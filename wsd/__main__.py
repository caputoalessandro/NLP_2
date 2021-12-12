import random

import nltk
import sys
from nltk.corpus import wordnet as wn, semcor
from nltk.corpus.reader import Lemma

from wsd.lesk import sentence_context, lesk, tokens_context, find_best_sense


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


def get_random_sentences_and_targets(tagged_corpus, n=50):
    sentences_and_targets = []

    for sentence in random.choices(tagged_corpus, k=n):
        target = pick_a_random_noun(sentence)

        if target is not None:
            sentences_and_targets.append(
                (
                    remove_tags(sentence),
                    target,
                )
            )

    if len(sentences_and_targets) < n:
        sentences_and_targets.extend(
            get_random_sentences_and_targets(
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


def main(n):
    if len(sys.argv) > 1:
        random.seed(sys.argv[1])

    accuracies = []
    baseline_accuracies = []

    for i in range(n):
        words_sentences = get_random_sentences_and_targets(
            semcor.tagged_sents(tag="sem")
        )
        results = [
            (lesk(target.name(), sentence), target)
            for sentence, target in words_sentences
        ]
        baseline = [
            (find_best_sense(target.name()), target)
            for _, target in words_sentences
        ]
        accuracies.append(accuracy(results))
        baseline_accuracies.append(accuracy(baseline))
        print(f"Round {i+1}: {accuracies[-1]:.2%}")
        print(f"Baseline: {baseline_accuracies[-1]:.2%}")

    mean = sum(accuracies) / len(accuracies)
    print(f"\nMean: {mean:.2%}")
    print(f"\nBase: {sum(baseline_accuracies) / len(baseline_accuracies) :.2%}")


if __name__ == "__main__":
    main(5)
