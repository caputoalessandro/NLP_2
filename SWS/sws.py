from annotation import make_correlations_file
from sense_identification import make
from evaluation import cohen_evaluation, print_accuracies


def semantic_similarity():
    # make_correlations_file()
    # make('caputo')
    # make('gentiletti')
    print("cohen score: ", cohen_evaluation())
    print_accuracies()


if __name__ == "__main__":
    semantic_similarity()

