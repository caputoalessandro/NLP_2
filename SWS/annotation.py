import csv
import os
from scipy.stats import pearsonr, spearmanr
from evaluation import nasari_correlations
from utils import get_rows


def means_from_pairs(l1, l2):
    return [(v1 + v2)/2 for v1, v2 in zip(l1, l2)]


def get_pairs_values():
    fp_1 = "resources/coppie_caputo.tsv"
    fp_2 = "resources/coppie_gentiletti.tsv"
    rows_1 = get_rows(fp_1)
    rows_2 = get_rows(fp_2)
    pairs = [(row[0], row[1]) for row in rows_1]
    v1 = [int(r[2]) for r in rows_1]
    v2 = [int(r[2]) for r in rows_2]
    return pairs, v1, v2


def get_data_to_write():
    pairs, v1, v2 = get_pairs_values()
    means = means_from_pairs(v1, v2)
    p_annotated, s_annotated = annotated_correlations(v1,v2)
    p_nasari, s_nasari = nasari_correlations(pairs,means)
    return pairs, means, p_annotated, s_annotated, p_nasari, s_nasari


def annotated_correlations(v1, v2):
    pearson = pearsonr(v1, v2)[0]
    spearman = spearmanr(v1, v2)[0]
    return pearson, spearman


def make_array_to_write():
    pairs, means, p_annotated, s_annotated, p_nasari, s_nasari = get_data_to_write()
    to_write = [(pair[0], pair[1], mean) for pair, mean in zip(pairs, means)]
    to_write.append(('-', '-', None))
    to_write.append(("Pearson_annotated", p_annotated, None))
    to_write.append(("Spearman_annotated", s_annotated, None))
    to_write.append(("Pearson_NASARI", p_nasari, None))
    to_write.append(("Spearman_NASARI", s_nasari, None))
    return to_write


def make_correlations_file():
    to_write = make_array_to_write()
    name = os.path.join("output", f"annotated_pairs.tsv")
    os.makedirs(os.path.dirname(name), exist_ok=True)
    
    with open(name, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(to_write)


