import itertools

import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset


def paths_upto_len(start: Synset, end: Synset, n):
    to_visit = [[start]]
    paths = []

    while to_visit:
        current_path = to_visit.pop()
        current_node = current_path[-1]

        if current_node == end:
            paths.append(current_path)
            continue

        if len(current_path) == n:
            continue

        next_paths = [[*current_path, next_node] for next_node in
                      itertools.chain(current_node.hyponyms(), current_node.hypernyms())]

        to_visit.extend(next_paths)

    return paths


def path_score(path):
    return np.exp(-(len(path) - 1))


def score(sense, frame_ctx, n=4):
    total = 0
    for frame_ctx_term in frame_ctx:
        for frame_ctx_sense in wn.synsets(frame_ctx_term):
            for path in paths_upto_len(sense, frame_ctx_sense, n):
                total += path_score(path)

    return total


def subgraph_mapper(word, frame_ctx):
    return max(wn.synsets(word), key=lambda s: score(s, frame_ctx))
