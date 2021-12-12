import itertools
from collections import deque
from functools import cache

import numpy as np
from nltk.corpus import wordnet as wn, framenet
from nltk.corpus.reader import Synset


VISITED_CACHE = {}


def paths_upto_len(start: Synset, end: Synset, n):
    queue = deque([[start]])
    paths = []

    while queue:
        current_path = queue.pop()
        current_node = current_path[-1]

        if current_node == end:
            paths.append(current_path)
            continue

        depth = len(current_path)

        if (current_node, end) in VISITED_CACHE:
            cached_depth, cached_paths = VISITED_CACHE[current_node, end]

            if cached_depth >= n - depth:
                paths.extend(path for path in cached_paths if len(path) <= n - depth)
                continue

        if depth == n:
            continue

        next_paths = [[*current_path, next_node] for next_node in
                      itertools.chain(current_node.hyponyms(), current_node.hypernyms())]
        if depth > 1:
            for last_node, cacheable_paths in itertools.groupby(next_paths, lambda p: p[-1]):
                cached_depth, _ = VISITED_CACHE.get((start, last_node), (0, []))
                if cached_depth < depth:
                    VISITED_CACHE[start, last_node] = depth, list(cacheable_paths)

        queue.extendleft(next_paths)

    cached_depth, _ = VISITED_CACHE.get((start, end), (0, []))
    if cached_depth < n:
        VISITED_CACHE[start, end] = n, paths

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
