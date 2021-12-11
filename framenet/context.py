from nltk.tokenize import word_tokenize
from wsd.lesk import synset_to_bag_of_words, sentence_to_bag_of_words


def sense_context(sense):
    context = set()

    for sense in (sense, *sense.hypernyms(), *sense.hyponyms()):
        context |= synset_to_bag_of_words(sense)

    return context


def frame_context(frame):
    context = set()

    for sentence in (frame.definition, *frame.FE.keys(), *map(lambda fe: fe.definition, frame.FE.values())):
        context |= sentence_to_bag_of_words(word_tokenize(sentence))

    return context
