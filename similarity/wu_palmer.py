from nltk.corpus import wordnet as wn
import csv


def lcs_search(s1, s2):
    common_subsumers = set()

    for p1 in s1.hypernym_paths():
        for p2 in s2.hypernym_paths():
            common_subsumers |= set(p1) & set(p2)

    if not common_subsumers:
        return None

    return max(common_subsumers, key=lambda k: k.min_depth())


def depth(s):
    return s.max_depth() + 1


def trough_lcs_depth(lcs,sub):
    return sub.shortest_path_distance(lcs) + depth(lcs)


def wu_palmer(synset1, synset2):
    cs = []

    for s1 in synset1:
        for s2 in synset2:
            lcs = lcs_search(s1, s2)

            if lcs:
                num = 2.0 * depth(lcs)
                denom = trough_lcs_depth(lcs, s1) + trough_lcs_depth(lcs, s2)
                cs.append(num / denom)
            else:
                cs.append(0)

    return max(cs)


def wp_similarity():
    reader = csv.reader(open("resources/WordSim353.csv"))
    cs = []

    for row in reader:
        synset1 = wn.synsets(row[0])
        synset2 = wn.synsets(row[1])

        if not synset1 or synset2:
            cs.append(0)

        else:
            cs.append(wu_palmer(synset1, synset2))

    return cs


if __name__ == "__main__":
    wp_similarity()

