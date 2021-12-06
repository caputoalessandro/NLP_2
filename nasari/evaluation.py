from utils import get_filtered_words
from collections import Counter


def reference_summary(text_path):
    f = open(text_path, "r")
    text = f.read()
    f_words = get_filtered_words(text)
    counts = Counter(f_words)
    return [w for w, v in counts.items() if v > 1]


def candidate_summary(summary):
    return get_filtered_words(summary)


def bleu(summary, text_path):
    retrivied = candidate_summary(summary)
    relevant = reference_summary(text_path)
    n = len(set(relevant) & set(retrivied))
    d = len(retrivied)
    return n/d


def rouge(summary, text_path):
    retrivied = candidate_summary(summary)
    relevant = reference_summary(text_path)
    n = len(set(relevant) & set(retrivied))
    d = len(relevant)
    return n/d