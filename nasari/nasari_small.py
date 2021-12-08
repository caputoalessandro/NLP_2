from pathlib import Path
from collections import defaultdict
from functools import cache

NASARI_SMALL_PATH = Path(__file__).parent.resolve() / 'resources' / 'dd-small-nasari-15.txt'


def parse_nasari_line(line: str):
    elems = line.rstrip().split(";")
    weights = {}

    for elem in elems[2:]:
        if elem == '':
            break
        elif '_' not in elem:
            continue

        lemma, weight = elem.split("_")
        weights[lemma] = float(weight)

    return elems[0], weights


@cache
def nasari_small_id_to_vector() -> dict[str, dict[str, float]]:
    with NASARI_SMALL_PATH.open() as lines:
        return dict(map(parse_nasari_line, lines))


@cache
def nasari_small_lemma_to_vector() -> dict[str, list[dict[str, float]]]:
    lemma_to_vectors = defaultdict(list)

    for vector in nasari_small_id_to_vector().values():
        for lemma in vector.keys():
            lemma_to_vectors[lemma].append(vector)

    return dict(lemma_to_vectors)
