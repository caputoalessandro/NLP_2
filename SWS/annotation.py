import csv
import os


def get_means_from_pairs(pairs):
    return [(v1 + v2)/2 for v1, v2 in pairs]


def get_rows(tsv):
    with open(tsv) as t:
        rows = csv.reader(t, delimiter="\t")
        return list(map(tuple, rows))


def get_pairs_values(fp_1, fp_2):
    rows_1 = get_rows(fp_1)
    rows_2 = get_rows(fp_2)
    pairs = [(row[0], row[1]) for row in rows_1]
    values = [(int(r1[2]), int(r2[2])) for r1, r2 in zip(rows_1, rows_2)]
    return pairs, values


def make_mean_file():
    fp_1 = "resources/coppie_caputo.tsv"
    fp_2 = "resources/coppie_gentiletti.tsv"

    pairs, values = get_pairs_values(fp_1, fp_2)
    means = get_means_from_pairs(values)

    name = os.path.join("output", f"annotated_pairs.tsv")
    os.makedirs(os.path.dirname(name), exist_ok=True)

    with open(name, "w") as f:
        for pair, mean in zip(pairs, means):
            f.write(pair[0]+'\t'+pair[1]+'\t'+str(mean)+'\n')
