from pathlib import Path

import numpy as np
from scipy.stats import spearmanr, pearsonr
from nasari_parser import get_nasari, get_synset_map
from sklearn.metrics import cohen_kappa_score
from utils import get_rows
import itertools
from utils import get_pairs_values


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
        return max([(s1, s2, cosine_similarity(nasari[s1], nasari[s2])) for s1 in synset_1 for s2 in synset_2 if nasari[s1] and nasari[s2]], key=lambda x: x[2])
    else:
        return (None, None, 0)


def get_all_cosine_similarity(pairs):
    return [max_cosine_similarity(w1, w2) for w1, w2 in pairs]


def nasari_correlations(pairs, means):
    args_sims = get_all_cosine_similarity(pairs)
    sims = [t[2] for t in args_sims]
    pearson = pearsonr(means, sims)[0]
    spearman = spearmanr(means, sims)[0]
    return pearson, spearman


ANNOTATED_PATH = Path(__file__).parent / 'annotated_files'


def get_gentiletti_caputo_babel_ids():
    caputo_rows = get_rows(ANNOTATED_PATH / 'coppie_caputo_babelid.tsv')
    caputo_list = list(itertools.chain(*[(p[2], p[3]) for p in caputo_rows]))
    caputo_pairs = [(p[2], p[3]) for p in caputo_rows]
    gentiletti_rows = get_rows(ANNOTATED_PATH / "coppie_gentiletti_babelid.tsv")
    gentiletti_list = list(itertools.chain(*[(p[2], p[3]) for p in gentiletti_rows]))
    gentiletti_pairs = [(p[2], p[3]) for p in gentiletti_rows]
    return caputo_list, caputo_pairs,gentiletti_list,gentiletti_pairs


def cohen_evaluation():
    caputo_list, caputo_pairs,gentiletti_list,gentiletti_pairs = get_gentiletti_caputo_babel_ids()
    return cohen_kappa_score(caputo_list, gentiletti_list)


def accuracy(nasari_pairs, nasari_list, ann_pairs, ann_list):
    pairs_accuracy = len(set(nasari_pairs) & set(ann_pairs)) / len(ann_pairs)
    acc = len(set(nasari_list) & set(ann_list)) / len(ann_list)
    return pairs_accuracy, acc


def print_accuracies():
    pairs, v1, v2 = get_pairs_values()
    args_sims = get_all_cosine_similarity(pairs)
    nasari_pairs = [(t[0], t[1]) for t in args_sims]
    nasari_list = list(itertools.chain(*[(p[0], p[1]) for p in nasari_pairs]))
    caputo_list, caputo_pairs, gentiletti_list, gentiletti_pairs = get_gentiletti_caputo_babel_ids()

    for student, single, pairs in [("Caputo",caputo_list, caputo_pairs), ("Gentiletti",gentiletti_list, gentiletti_pairs)]:
        pairs_acc, acc = accuracy(nasari_pairs, nasari_list, pairs, single)
        print("--------------------------------------")
        print(student)
        print("pairs accuracy: ", pairs_acc)
        print("single word accuracy: ", acc)
