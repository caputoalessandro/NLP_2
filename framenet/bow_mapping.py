from dataclasses import dataclass

from typing import Any

from nltk.corpus.reader import Synset

from utils import is_multiword, get_regent, get_frame_from_id_list
from context import frame_context, sense_context
from nltk.corpus import wordnet as wn, framenet
from tabulate import tabulate

ids_caputo = [1594, 422, 1812, 2140, 118]
ids_gentiletti = [308, 1943, 2430, 333, 381]


WHITELIST = {
    'trans-shipping': 'transshipping',
    'possession_[definite_noun]': 'possession',
    'possession_[of_goods]': 'possession'
}


def choose_word_to_map(word):
    if word in WHITELIST:
        return WHITELIST[word]
    if len(wn.synsets(word)) > 0:
        return word
    elif is_multiword(word):
        return choose_word_to_map(get_regent(word))
    else:
        raise ValueError(f'Non sono presenti sensi WordNet per "{word}".')


def map_word(word, frame_ctx):
    word = choose_word_to_map(word)

    max_score = 0
    best_sense = None

    for sense in wn.synsets(word):
        sense_ctx = sense_context(sense)
        score = len(frame_ctx & sense_ctx) + 1

        if score > max_score:
            max_score = score
            best_sense = sense

    return best_sense


def map_fes(frame, frame_ctx):
    return {fe.name: map_word(fe.name, frame_ctx) for fe in frame.FE.values()}


def map_lus(frame, frame_ctx):
    mapped_lus = {}

    for lu in frame.lexUnit.values():
        name = lu.name.rsplit('.', 1)[0].replace(' ', '_')
        mapped_lus[name] = map_word(name, frame_ctx)

    return mapped_lus


@dataclass
class FrameMapping:
    frame: Any
    name: tuple[str, Synset]
    frame_elements: dict[str, Synset]
    lexical_units: dict[str, Synset]

    def __str__(self):
        return f"""
------------------------------------------------------------
Mapping for frame "{self.frame.name}". {len(self.frame_elements)} FEs and {len(self.lexical_units)} LUs.

{self.name[0]}\t{self.name[1].name()}

# Frame Elements

{tabulate([(name, synset.name()) for name, synset in self.frame_elements.items()], tablefmt='plain')}

# Lexical Units

{tabulate([(name, synset.name()) for name, synset in self.lexical_units.items()], tablefmt='plain')}
"""


def map_frame(frame):
    frame_ctx = frame_context(frame)

    mapped_name = map_word(frame.name, frame_ctx)
    mapped_fes = map_fes(frame, frame_ctx)
    mapped_lus = map_lus(frame, frame_ctx)

    return FrameMapping(frame, (choose_word_to_map(frame.name), mapped_name), mapped_fes, mapped_lus)


def bow_mapping():
    frames = [framenet.frame(i) for i in ids_caputo + ids_gentiletti]
    return [map_frame(frame) for frame in frames]


if __name__ == "__main__":
    for mapping in bow_mapping():
        print(mapping)
