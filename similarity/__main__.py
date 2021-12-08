import csv
from textwrap import dedent

from scipy.stats import pearsonr, spearmanr

from similarity.similarity_measures import wu_palmer, shortest_path, leakcock_chodorow

from nltk.corpus import wordnet as wn


def wordsim353():
    term_pairs = []
    scores = []

    with open('resources/WordSim353.csv') as lines:
        for term1, term2, score in csv.reader(lines):
            term_pairs.append((term1, term2))
            scores.append(float(score))

    return term_pairs, scores


def term_similarity(sense_similarity, term1, term2):
    synsets1 = wn.synsets(term1)
    synsets2 = wn.synsets(term2)

    return max((sense_similarity(s1, s2) for s1 in synsets1 for s2 in synsets2), default=0)


def main():
    term_pairs, golden = wordsim353()
    for sense_similarity in (wu_palmer, shortest_path, leakcock_chodorow):
        scores = [term_similarity(sense_similarity, term1, term2) for term1, term2 in term_pairs]
        print(dedent(f"""
        {sense_similarity.__name__}
        Pearson:  {pearsonr(scores, golden)[0]:.2f}
        Spearman: {spearmanr(scores, golden)[0]:.2f}
        """))


if __name__ == "__main__":
    main()
