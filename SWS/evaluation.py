import numpy as np
from nasari_parser import get_nasari, get_synset_map
from similarity.correlations import correlation


def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)
    num = np.inner(v1, v2)
    denom = v1_norm * v2_norm
    return num/denom


def max_cosine_similarity(w1, w2):
    syn_map = get_synset_map()
    nasari = get_nasari()

    synset_1 = syn_map[w1]
    synset_2 = syn_map[w2]

    if synset_1 and synset_2:
        return max(cosine_similarity(nasari[s1], nasari[s2]) for s1 in synset_1 for s2 in synset_2 if nasari[s1] and nasari[s2])
    else:
        return 0


def get_all_cosine_similarity(pairs):
    return [max_cosine_similarity(w1, w2) for w1, w2 in pairs]


def nasari_correlations(pairs, means):
    sims = get_all_cosine_similarity(pairs)
    pearson = correlation(means, sims, "pearson")
    spearman = correlation(means, sims, "spearman")
    return pearson, spearman

