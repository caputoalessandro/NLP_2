from nltk.corpus import wordnet as wn

from framenet.context import frame_context
from framenet.frame_mapping import FrameMapping
from framenet.utils import is_multiword, get_regent


WHITELIST = {
    'trans-shipping': 'transshipping',
    'possession_[definite_noun]': 'possession',
    'possession_[of_goods]': 'possession'
}


def choose_word_to_map(word):
    word = word.lower()

    if word in WHITELIST:
        return WHITELIST[word]
    if len(wn.synsets(word)) > 0:
        return word
    elif is_multiword(word):
        return choose_word_to_map(get_regent(word))
    else:
        raise ValueError(f'Non sono presenti sensi WordNet per "{word}".')


def normalized_lu_name(word):
    return word.rsplit('.', 1)[0].replace(' ', '_')


def map_frame(frame, map_word):
    frame_ctx = frame_context(frame)

    def map_words(words):
        return {word: map_word(choose_word_to_map(word), frame_ctx) for word in words}

    mapped_name = map_words([frame.name])
    mapped_fes = map_words(frame.FE)
    mapped_lus = map_words(normalized_lu_name(lu) for lu in frame.lexUnit)

    return FrameMapping(frame, mapped_name, mapped_fes, mapped_lus)


