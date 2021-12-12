import numpy as np
from nltk.corpus import wordnet as wn, framenet
from nltk.corpus.reader import Synset


def paths_upto_len(start: Synset, end: Synset, n):
    if n <= 0:
        return []

    if start == end:
        return [[start]]

    paths = []

    for next_node in [*start.hyponyms(), *start.hypernyms()]:
        paths.extend(p for p in paths_upto_len(next_node, end, n-1) if p is not None)

    for path in paths:
        path.insert(0, start)

    return paths


def path_score(path):
    return np.exp(-(len(path) - 1))


def score(sense, frame_ctx, n=3):
    total = 0
    for frame_ctx_term in frame_ctx:
        for frame_ctx_sense in wn.synsets(frame_ctx_term):
            for path in paths_upto_len(sense, frame_ctx_sense, n):
                total += path_score(path)

    return total


def subgraph_mapper(word, frame_ctx):
    return max(wn.synsets(word), key=lambda s: score(s, frame_ctx))
