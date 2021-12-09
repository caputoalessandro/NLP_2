from nasari_parser import get_synset_map, get_nasari
from nasari.nasari_small import nasari_small_id_to_vector
from annotation import get_pairs_values
from babelnet import get_dict_from_json
import itertools
from utils import save_dict


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
            synset_id: get_lemmas_from_synset(synset_id, nasari, missed)[:3]
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




