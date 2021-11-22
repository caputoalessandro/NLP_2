from utils import is_multiword, get_regent, get_frame_from_id_list
from context import frame_context, sense_context
from nltk.corpus import wordnet as wn

ids_caputo = [1594, 422, 1812, 2140, 118]
ids_gentiletti = [308, 1943, 2430, 333, 381]


def map_word(word, frame_context):

    max_score = 0
    best_sense = None

    for sense in wn.synsets(word):
        s_context = sense_context(sense)
        score = len(frame_context & s_context) + 1

        if score > max_score:
            max_score = score
            best_sense = sense

    return word, best_sense


def map_fes(frame, frame_context):
    res = []

    for fe in frame.FE.values():
        frame_name = fe.name
        if is_multiword(frame_name):
            frame_name = get_regent(frame_name)

        res.append(map_word(frame_name, frame_context))

    return res


def map_lus(frame, frame_context):
    res = []

    for lu in frame.lexUnit.values():
        word = lu.name.rsplit(".", 1)[0]
        if not word:
            continue
        word = word.replace(' ', '_')
        res.append(map_word(word, frame_context))

    return res


def map_name(frame_name, frame_context):
    if is_multiword(frame_name):
        frame_name = get_regent(frame_name)

    return map_word(frame_name, frame_context)


def bow_mapping():

    frames = get_frame_from_id_list(ids_caputo + ids_gentiletti)
    mapping = None

    for frame in frames:
        f_context = set(frame_context(frame))

        mapped_name = map_name(frame.name, f_context)
        mapped_fes = map_fes(frame, f_context)
        mapped_lus = map_lus(frame, f_context)
        mapping = mapped_name, mapped_fes, mapped_lus

    return mapping


if __name__ == "__main__":
    bow_mapping()