from nasari_parser import get_synset_map, get_nasari
from nasari.nasari_small import nasari_small_id_to_vector
from annotation import get_pairs_values
from babelnet import get_dict_from_json
import itertools
from utils import save_dict,get_rows
import os, csv
from caputo_babel_ids import get_babel_id_caputo


def get_synsets_from_word(word, syn_map):
    return [synset for synset in syn_map[word]]


def get_lemmas_from_synset(synset_id, nasari, missed):
    if synset_id in nasari.keys():
        return list(nasari[synset_id].keys())
    elif synset_id in missed.keys():
        if missed[synset_id] is None:
            return []
        else:
            return missed[synset_id]


def get_word_lemmas(word, syn_map, nasari, missed):
    return {
            synset_id: get_lemmas_from_synset(synset_id, nasari, missed)
            for synset_id in get_synsets_from_word(word, syn_map)
         }


def get_words_syns_lemmas(words, syn_map, nasari, missed):
    return {word: get_word_lemmas(word, syn_map, nasari, missed) for word in words}


def get_reources():
    pairs, v1, v2 = get_pairs_values()
    words = list(itertools.chain(*pairs))
    nasari = nasari_small_id_to_vector()
    syn_map = get_synset_map()
    missed = get_dict_from_json()
    return words, syn_map, nasari, missed


def get_words_syns_lemmas_from_wordlist():
    words, syn_map, nasari, missed = get_reources()
    words_syns_lemmas = get_words_syns_lemmas(words, syn_map, nasari, missed)
    save_dict("words_syns_lemmas.json", words_syns_lemmas)
    return words_syns_lemmas


def get_three_lemmas(lemmas):
    result = []
    for lemma in lemmas:
        if lemma not in result:
            result.append(lemma)
        if len(result) == 3:
            return result
    return result


def get_data_to_write(surname):
    pairs_ids = []
    wsl = get_words_syns_lemmas_from_wordlist()
    pairs, v1, v2 = get_pairs_values()
    if surname == "caputo":
        pairs_ids = get_babel_id_caputo()
    elif surname == "gentiletti":
        pairs_ids = get_babel_ids_gentiletti()
    return pairs, pairs_ids, wsl


def get_babel_ids_gentiletti():
    rows = get_rows("resources/coppie_gentiletti_babelid.tsv")
    return [(p[2], p[3]) for p in rows]


def make_array_to_write(surname):
    result = []
    pairs, pairs_ids, wsl = get_data_to_write(surname)
    for p, s in zip(pairs, pairs_ids):
        lemmas_1 = []
        lemmas_2 = []
        if s[0] is not None and s[0] != 'None' and s[0] in wsl[p[0]].keys():
            lemmas_1 = get_three_lemmas(wsl[p[0]][s[0]])
        if s[1] is not None and s[1] != 'None' and s[1] in wsl[p[1]].keys():
            lemmas_2 = get_three_lemmas(wsl[p[1]][s[1]])
        result.append((p[0], p[1], s[0], s[1], lemmas_1, lemmas_2))
    return result


def make(surname):
    to_write = make_array_to_write(surname)
    name = os.path.join("output", f"coppie_gentiletti_babelid.tsv")
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(to_write)
