from nltk.tokenize import word_tokenize
from wsd.lesk import synset_context, sentence_context


def sense_context(sense):
    context = set()

    for sense in (sense, *sense.hypernyms(), *sense.hyponyms()):
        context |= synset_context(sense)

    return context


def frame_context(frame):
    context = set()

    for sentence in (frame.definition, *frame.FE.keys(), *map(lambda fe: fe.definition, frame.FE.values())):
        context |= sentence_context(sentence)

    return context
