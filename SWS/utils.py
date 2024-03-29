import csv
import json
from pathlib import Path


def get_rows(tsv):
    with open(tsv) as t:
        rows = csv.reader(t, delimiter="\t")
        return list(map(tuple, rows))


def save_dict(file_name, data):
    a_file = open("resources/" + file_name, "w")
    json.dump(data, a_file, indent=4)


RESOURCES_PATH = Path(__file__).parent / 'resources'


def get_pairs_values():
    fp_1 = RESOURCES_PATH / "coppie_caputo.tsv"
    fp_2 = RESOURCES_PATH / "coppie_gentiletti.tsv"
    rows_1 = get_rows(fp_1)
    rows_2 = get_rows(fp_2)
    pairs = [(row[0], row[1]) for row in rows_1]
    v1 = [int(r[2]) for r in rows_1]
    v2 = [int(r[2]) for r in rows_2]
    return pairs, v1, v2


