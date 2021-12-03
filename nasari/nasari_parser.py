from dataclasses import dataclass, field
from logging import getLogger
from collections import defaultdict
from typing import Dict, Iterable, Iterator, Mapping

logger = getLogger(__name__)


@dataclass(eq=True, frozen=True)
class NasariVector:
    synset_id: str
    wikipedia_title: str
    weights: Mapping[str, float] = field(hash=False)


def parse_nasari_vector(line: str) -> NasariVector:
    elems = line.rstrip().split(";")
    weights = {}
    for elem in elems[2:]:
        if elem == "":
            continue
        lemma, weight = elem.split("_")
        weights[lemma] = float(weight)
    return NasariVector(elems[0], elems[1], weights)


def read_nasari_resource(lines: Iterable[str]) -> Iterator[NasariVector]:
    for i, line in enumerate(lines):
        try:
            yield parse_nasari_vector(line)
        except ValueError:
            logger.info(f"Line {i}: {line}", exc_info=True)
            continue


def build_lemma_index(vectors: Iterable[NasariVector]):
    result = defaultdict(set)

    for vector in vectors:
        for lemma in vector.weights.keys():
            result[lemma].add(vector)

    return dict(result)


