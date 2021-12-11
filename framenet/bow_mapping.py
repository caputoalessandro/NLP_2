from framenet.frame_mapping import FrameMapping
from framenet.utils import is_multiword, get_regent
from framenet.context import frame_context, sense_context
from nltk.corpus import wordnet as wn, framenet

ids_caputo = [1594, 422, 1812, 2140, 118]
ids_gentiletti = [308, 1943, 2430, 333, 381]


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


def map_words(words, frame_ctx):
    return {word: map_word(word, frame_ctx) for word in words}


def normalized_lu_name(word):
    return word.rsplit('.', 1)[0].replace(' ', '_')


def map_frame(frame):
    frame_ctx = frame_context(frame)

    mapped_name = map_words([frame.name], frame_ctx)
    mapped_fes = map_words(frame.FE, frame_ctx)
    mapped_lus = map_words(map(normalized_lu_name, frame.lexUnit), frame_ctx)

    return FrameMapping(frame, mapped_name, mapped_fes, mapped_lus)


def bow_mapping():
    frames = [framenet.frame(i) for i in ids_caputo + ids_gentiletti]
    return [map_frame(frame) for frame in frames]


if __name__ == "__main__":
    for mapping in bow_mapping():
        print(mapping)
