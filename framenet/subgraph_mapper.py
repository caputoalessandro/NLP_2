import itertools
from functools import cache

import numpy as np
from nltk.corpus import wordnet as wn, framenet
from nltk.corpus.reader import Synset


VISITED_CACHE = {}


def paths_upto_len(start: Synset, end: Synset, n):
    stack = [[start]]
    paths = []

    while stack:
        current_path = stack.pop()
        current_node = current_path[-1]

        if current_node == end:
            paths.append(current_path)
            continue

        if (current_node, end) in VISITED_CACHE:
            cached_paths, cached_depth = VISITED_CACHE[current_node, end]

            threshold = n - len(current_path)
            if cached_depth >= threshold:
                paths.append([path for path in cached_paths if len(path) <= threshold])
                continue

        if len(current_path) == n:
            continue

        next_paths = [[*current_path, next_node] for next_node in
                      itertools.chain(current_node.hyponyms(), current_node.hypernyms())]

        stack.extend(next_paths)
        # VISITED_CACHE[]

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
