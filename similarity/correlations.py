import numpy as np
import csv
from similarity.wu_palmer import wp_similarity


def get_target():
    # estraggo valori target
    y = []
    reader = csv.reader(open("resources/WordSim353.csv"))
    for row in reader:
        y.append(float(row[2]))

    return y


def correlation(x, y, type):

    num = None
    denom = None

    x_array = np.array(x)
    y_array = np.array(y)

    if type == "pearson":
        num = np.cov(x_array, y_array)[0][1]
        denom = np.std(x_array) * np.std(y_array)

    elif type == "spearman":
        order_x = x_array.argsort()
        x_ranks = order_x.argsort()
        order_y = y_array.argsort()
        y_ranks = order_y.argsort()
        num = np.cov(x_ranks, y_ranks)[0][1]
        denom = np.std(x_ranks) * np.std(y_ranks)

    else:
        print("ERRORE: indicare tipo di correlazione")

    return num / denom


def correlations(sim, type):

    y = get_target()

    if sim == "wup":
        return correlation(wp_similarity(), y, type)

    elif sim == "shortest":
        return 0

    elif sim == "lc":
        return 0

