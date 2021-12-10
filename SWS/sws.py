from annotation import make_correlations_file
from sense_identification import get_words_syns_lemmas_from_wordlist
from sense_identification import make
from evaluation import cohen_evaluation, print_accuracies
from nasari.nasari_small import nasari_small_id_to_vector


def semantic_similarity():
    # make_correlations_file()
    # make('caputo')
    # make('gentiletti')
    print("cohen score: ", cohen_evaluation())
    print_accuracies()


if __name__ == "__main__":
    semantic_similarity()

