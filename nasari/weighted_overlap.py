import pandas as pd


def get_ranks(vector):
    return pd.Series(vector).rank()


def weighted_overlap(v1, v2):
    o = v1.keys() & v2.keys()
    v1_ranks = get_ranks(v1)
    v2_ranks = get_ranks(v2)
    if not o:
        return 0
    else:
        return (len(o) * (len(o) + 1)) / sum(v1_ranks[q] + v2_ranks[q] for q in o)
