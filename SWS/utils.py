import csv
import json


def get_rows(tsv):
    with open(tsv) as t:
        rows = csv.reader(t, delimiter="\t")
        return list(map(tuple, rows))


def save_dict(file_name, data):
    a_file = open("resources/" + file_name, "w")
    json.dump(data, a_file, indent=4)




