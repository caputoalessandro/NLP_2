from annotation import make_scores_file
from sense_identification import make_babel_id_file
from evaluation import cohen_evaluation, print_accuracies


def main():
    make_scores_file()
    make_babel_id_file('caputo')
    make_babel_id_file('gentiletti')
    print("cohen score: ", cohen_evaluation())
    print_accuracies()


if __name__ == "__main__":
    main()

