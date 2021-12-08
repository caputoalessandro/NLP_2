from itertools import chain
from math import log

from nltk.corpus.reader import Synset

WN_MAX_DEPTH = 19


def lcs_search(s1, s2):
    s1_ancestors = set(chain.from_iterable(s1.hypernym_paths()))
    s2_ancestors = set(chain.from_iterable(s2.hypernym_paths()))
    common_subsumers = s1_ancestors & s2_ancestors

    return max(common_subsumers, key=lambda k: k.min_depth(), default=None)


def depth(s):
    return s.max_depth() + 1


def trough_lcs_depth(lcs,sub):
    return sub.shortest_path_distance(lcs) + depth(lcs)


def wu_palmer(s1, s2):
    lcs = lcs_search(s1, s2)

    if not lcs:
        return 0

    num = 2.0 * depth(lcs)
    denom = trough_lcs_depth(lcs, s1) + trough_lcs_depth(lcs, s2)
    return num / denom


def shortest_path(s1: Synset, s2: Synset):
    return (WN_MAX_DEPTH + 1) * 2 - s1.shortest_path_distance(s2, simulate_root=True)


def leakcock_chodorow(s1: Synset, s2: Synset):
    return -log((s1.shortest_path_distance(s2, simulate_root=True) + 1) / ((WN_MAX_DEPTH + 1) * 2) + 1)
