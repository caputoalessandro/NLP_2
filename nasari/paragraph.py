from utils import get_filtered_title, get_filtered_words, disambiguation, write, not_stop_or_punct
from weighted_overlap import weighted_overlap
import pandas as pd
import itertools
import os


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


def get_ranked_paragraphs(paragraphs, text_path):
    ranked_by_title = rank_by_title(paragraphs, text_path)
    ranked_by_cohesion = rank_by_cohesion(paragraphs)
    p_list_title = [p + "\n" for p in ranked_by_title.index]
    p_list_cohesion = [p + "\n" for p in ranked_by_cohesion.index]
    return "".join(p_list_title), "".join(p_list_cohesion)


def ordered_paragraph_by_score(text_path, context, nasari):
    paragraphs = get_paragraphs(text_path)
    p_scores = paragraphs_scores(paragraphs, context, text_path, nasari)
    p_scores.sort(key=lambda tup: tup[1], reverse=True)
    return [p for p, v in p_scores]


def compress(ordered_paragraphs, compression):
    to_keep = int(len(ordered_paragraphs) - ((len(ordered_paragraphs) / 100) * compression))
    return ordered_paragraphs[:to_keep]


def write_ranked_paragraphs(paragraphs, text_path, compression):
    by_title, by_cohesion = get_ranked_paragraphs(paragraphs, text_path)
    write(os.path.basename(text_path), by_title, compression, "title")
    write(os.path.basename(text_path), by_cohesion, compression, "cohesion")
    return by_title, by_cohesion


# def get_salient_paragraphs(text_path, context, compression, ranking_type, nasari, type):
#     ordered_paraghraps = ordered_paragraph_by_score()
#     to_keep = int(len(paragraphs) - ((len(paragraphs) / 100) * compression))
#     output = get_ranked_paragraphs(ordered_paraghraps[:to_keep], text_path, ranking_type)
#     write(os.path.basename(text_path), output, compression, type)
#     return output


def get_paragraphs(text_path):
    with open(text_path, "r") as f:
        text = f.read()
        return text.split('\n\n')


def paragraphs_scores(paragraphs, context, text_path, nasari):
    return [(p, paragraph_score(p, context, text_path, nasari)) for p in paragraphs]


def paragraph_score(paragraph, context, text_path, nasari):
    return sum(word_score(word, context, text_path, nasari) for word in paragraph if not_stop_or_punct(word))


def word_score(word, context, text_path, nasari):
    if not word in nasari.keys():
        return 0
    dis_vector = disambiguation(nasari[word], text_path)
    return sum(weighted_overlap(dis_vector, v) for v in context.values())