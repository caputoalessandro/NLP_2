from utils import get_filtered_title, get_lemmas_from_source, get_filtered_words,  get_dis_vectors,disambiguation
from weighted_overlap import weighted_overlap
import pandas as pd
import itertools


def rank_paragraphs(p_freq):
    sr = pd.Series(p_freq.values())
    sr.index = p_freq.keys()
    return sr.rank().sort_values(ascending=False)


def rank_by_title(paragraphs, text_path):
    title = get_filtered_title(text_path)
    p_freqs = {p: len(set(p) & set(title)) for p in paragraphs}
    return rank_paragraphs(p_freqs)


def rank_by_cohesion(paragraphs):
    p_freqs = {}

    for p, other in itertools.permutations(paragraphs, 2):
        p_freqs.setdefault(p, 0)
        p_freqs[p] = p_freqs[p] + len(set(p) & set(other))

    return rank_paragraphs(p_freqs)


def get_ranked_paragraphs(paragraphs, text_path, type):

    if type == "title":
        ranked_p = rank_by_title(paragraphs, text_path)
    elif type == "cohesion":
        ranked_p = rank_by_cohesion(paragraphs)
    else:
        print("specifica il tipo  di ranking")
        return 0

    return [p for p in ranked_p.index]


def get_salient_paragraphs(text_path, context, compression, ranking_type):
    paragraphs = get_paragraphs(text_path)
    p_scores = paragraphs_scores(paragraphs, context, text_path)
    p_scores.sort(key=lambda tup: tup[1], reverse=True)
    ordered_paraghraps = [p for p, v in p_scores]
    to_keep = int((len(paragraphs) / 100) * compression)
    return get_ranked_paragraphs(ordered_paraghraps[:to_keep], text_path, ranking_type)


def get_paragraphs(text_path):
    f = open(text_path, "r")
    text = f.read()
    return text.split('\n\n')


def paragraphs_scores(paragraphs, context, text_path):
    return [(p, paragraph_score(p, context, text_path)) for p in paragraphs]


def paragraph_score(paragraph, context, text_path):
    return sum(word_score(word, context, text_path) for word in get_filtered_words(paragraph))


def word_score(word, context, text_path):
    nasari = get_lemmas_from_source()

    if not word in nasari.keys():
        return 0

    dis_vector = disambiguation(nasari[word], text_path)
    return sum(weighted_overlap(dis_vector, v) for v in context.values())

