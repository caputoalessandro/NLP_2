from utils import preprocessing

from wsd.lesk import synset_to_bag_of_words


def hyper_context(sense):
    context = set()
    for hyper in sense.hypernyms():
        context |= synset_to_bag_of_words(hyper)
    return context


def hypo_context(sense):
    context = set()
    for hypo in sense.hyponyms():
        context |= synset_to_bag_of_words(hypo)
    return context


def sense_context(sense):
    return (
        synset_to_bag_of_words(sense)
        .union(hyper_context(sense))
        .union(hypo_context(sense))
    )


def frame_elements_defs(frame):
    context = []
    for fe in frame.FE.values():
        context = context + preprocessing(fe.definition)
    return context


def frame_context(frame):
    frame_def = preprocessing(frame.definition)
    fes_def = frame_elements_defs(frame)
    return frame_def + fes_def
