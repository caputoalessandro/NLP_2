from correlations import correlations

wup = "wup"
shortest = "shortest"
lc = "lc"
pearson = "pearson"
spearman = "spearman"


def similarity():

    print(correlations(wup, spearman))

    return 0


if __name__ == "__main__":
    similarity()