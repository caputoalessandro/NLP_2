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


def get_ranked_paragraphs(paragraphs, text_path, type):

    if type == "title":
        ranked_p = rank_by_title(paragraphs, text_path)
    elif type == "cohesion":
        ranked_p = rank_by_cohesion(paragraphs)
    else:
        print("specifica il tipo  di ranking")
        return 0

    res = [p + "\n" for p in ranked_p.index]
    return "".join(res)


def get_salient_paragraphs(text_path, context, compression, ranking_type, nasari, type):
    paragraphs = get_paragraphs(text_path)
    p_scores = paragraphs_scores(paragraphs, context, text_path, nasari)
    p_scores.sort(key=lambda tup: tup[1], reverse=True)
    ordered_paraghraps = [p for p, v in p_scores]
    to_keep = int(len(paragraphs) - ((len(paragraphs) / 100) * compression))
    output = get_ranked_paragraphs(ordered_paraghraps[:to_keep], text_path, ranking_type)
    write(os.path.basename(text_path), output, compression, type)
    return output


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