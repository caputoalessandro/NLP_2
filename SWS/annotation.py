import csv
import os


def get_mean_from_pairs(pairs):
    return [(v1 + v2)/2 for v1, v2 in pairs]


def get_pairs_values(fp_1, fp_2):
    with open(fp_1) as f1:
        rows = csv.reader(f1, delimiter="\t")
        pairs = [(row[0], row[1]) for row in rows]
        value_1 = [float(row[2]) for row in rows]

    with open(fp_2) as f2:
        rows = csv.reader(f2, delimiter="\t")
        value_2 = [float(row[2]) for row in rows]

    return pairs, [(v1, v2) for v1, v2 in zip(value_1, value_2)]


def make_mean_file():
    fp_1 = "resources/coppie_caputo.tsv"
    fp_2 = "resources/coppie_gentiletti.tsv"

    pairs, values = get_pairs_values(fp_1, fp_2)
    means = get_mean_from_pairs(values)

    name = os.path.join("output", f"annotated_pairs.txt")
    os.makedirs(os.path.dirname(name), exist_ok=True)

    with open(name, "w") as f:
        for pair,  mean in zip(pairs, means):
            f.write(str(pair)+str(mean))
