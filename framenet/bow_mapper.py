from nltk.corpus import wordnet as wn

from framenet.context import sense_context


def bow_mapper(word, frame_ctx):
    max_score = 0
    best_sense = None

    for sense in wn.synsets(word):
        sense_ctx = sense_context(sense)
        score = len(frame_ctx & sense_ctx) + 1

        if score > max_score:
            max_score = score
            best_sense = sense

    return best_sense
