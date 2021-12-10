import os

from nltk.corpus import wordnet as wn
from tabulate import tabulate
import textwrap

from framenet.bow_mapping import bow_mapping, choose_word_to_map, frame_context


def wrap(text):
    return '\n'.join(textwrap.wrap(text, width=50))


def wrap_row(t):
    return tuple(map(wrap, t))


def lemmas_description(synset):
    return ', '.join(map(lambda l: l.name(), synset.lemmas()))


def synset_info_table(word):
    synsets = wn.synsets(word)
    os.system('clear')

    headers = ['Synset', 'Definizione', 'Lemmi']

    rows = [
        wrap_row((synset.name(), synset.definition(), lemmas_description(synset)))
        for synset in synsets
    ]

    return tabulate(rows, headers, showindex=True, tablefmt='fancy_grid')


def frame_info_table(frame):
    headers = ['Frame', 'Definizione', 'Contesto']
    frame_ctx_description = ', '.join(sorted(frame_context(frame)))
    return tabulate([wrap_row((frame.name, frame.definition, frame_ctx_description))], headers, tablefmt='fancy_grid')


BACK = object()


def input_prompt(synsets_len):
    while True:
        try:
            answer = input("Inserisci indice del synset o 'z' per tornare alla parola precedente: ")

            if answer == 'z':
                return BACK

            answer = int(answer)

            if 0 <= answer < synsets_len:
                return answer

        except ValueError:
            continue


def main():
    for f_map in bow_mapping():
        for term in (f_map.name[0], *f_map.frame_elements.keys(), *f_map.lexical_units.keys()):
            print(synset_info_table(term))
            print(frame_info_table(f_map.frame))



if __name__ == '__main__':
    main()
