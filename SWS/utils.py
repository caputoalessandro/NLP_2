import csv


def get_rows(tsv):
    with open(tsv) as t:
        rows = csv.reader(t, delimiter="\t")
        return list(map(tuple, rows))

