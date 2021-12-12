import os

from nltk.corpus import wordnet as wn, framenet
from tabulate import tabulate
import textwrap

from framenet.context import (frame_context,)
from framenet.map_frame import choose_word_to_map, normalized_lu_name
from framenet.__main__ import ids_caputo, ids_gentiletti
from framenet.frame_mapping import FrameMapping, yaml
from framenet.utils import mapkeys


def wrap(text):
    return "\n".join(textwrap.wrap(text, width=50))


def wrap_row(t):
    return tuple(map(wrap, t))


def lemmas_description(synset):
    return ", ".join(map(lambda l: l.name(), synset.lemmas()))


def synset_info_table(synsets):
    headers = ["Synset", "Definizione", "Lemmi"]

    rows = [
        wrap_row(
            (synset.name(), synset.definition(), lemmas_description(synset))
        )
        for synset in synsets
    ]

    return tabulate(rows, headers, showindex=True, tablefmt="fancy_grid")


def frame_info_table(frame):
    headers = ["Frame", "Definizione", "Contesto"]
    frame_ctx_description = ", ".join(sorted(frame_context(frame)))
    return tabulate(
        [wrap_row((frame.name, frame.definition, frame_ctx_description))],
        headers,
        tablefmt="fancy_grid",
    )


def term_info_table(term, term_attrs):
    headers = ["Termine", "Normalizzato", "Definizione"]
    return tabulate(
        [
            wrap_row(
                (term, choose_word_to_map(term), term_attrs.get("definition", ''))
            )
        ],
        headers,
        tablefmt="fancy_grid",
    )


def input_prompt(synsets):
    while True:
        try:
            answer = input("Inserisci indice del synset: ")
            answer = int(answer)

            if 0 <= answer < len(synsets):
                return synsets[answer]
        except ValueError:
            continue


def ask_annotation_for_terms(frame, terms: dict[str, dict]):
    term_map = {}
    for term, term_attrs in terms.items():
        synsets = wn.synsets(choose_word_to_map(term))
        if len(synsets) == 1:
            term_map[term] = synsets[0]
        else:
            os.system("clear")
            print(synset_info_table(synsets))
            print(term_info_table(term, term_attrs))
            print(frame_info_table(frame))
            term_map[term] = input_prompt(synsets)
    return term_map


def main():
    frames = [framenet.frame(i) for i in ids_caputo + ids_gentiletti]
    annotated_f_maps = []

    for frame in frames:
        frame_mappings = []
        for terms in {frame.name: {}}, frame.FE, mapkeys(normalized_lu_name, frame.lexUnit):
            frame_mappings.append(ask_annotation_for_terms(frame, terms))

        annotated_f_maps.append(FrameMapping(frame, *frame_mappings))

    with open("resources/annotations.yaml", "w") as output:
        yaml.dump(annotated_f_maps, output)


if __name__ == "__main__":
    main()
