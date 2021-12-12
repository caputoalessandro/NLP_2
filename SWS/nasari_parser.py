from pathlib import Path

from utils import get_rows
from collections import defaultdict

RESOURCES_PATH = Path(__file__).parent / 'resources'


def get_lines():
    fp = RESOURCES_PATH / "SemEval17_IT_senses2synsets.txt"
    with open(fp) as f:
        lines = f.readlines()
    return lines


def get_synset_map():
    lines = get_lines()
    result = defaultdict(set)
    s_list = []
    key = None

    for line in lines:
        if "#" in line:
            if key and s_list:
                result[key] = s_list
                s_list = []
            key = line[1:-1]
        else:
            s_list.append(line[:-1])

    return result


def get_id_weights(row):
    synset_id, lemma = str(row[0]).split("__")
    weights = [float(weight) for weight in row[2:]]
    return synset_id, weights


def get_nasari():
    p = RESOURCES_PATH / "mini_NASARI.tsv"
    result = defaultdict(set)
    rows = get_rows(p)

    for row in rows:
        id, weights = get_id_weights(row)
        result[id] = weights

    return result
