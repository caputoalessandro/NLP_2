import os
import requests
import json
from nasari import nasari_small
from annotation import get_pairs_values
from nasari_parser import get_synset_map
from typing import Dict
from utils import save_dict


BABELNET_BASE_URL = "https://babelnet.io/v6"


class BabelNetClient:
    def __init__(self, key=os.getenv("BABELNET_KEY")):
        if key is None:
            raise ValueError("BabelNet API key not provided.")

        self.session = requests.Session()
        self.session.params["key"] = key

    def get_synset_ids(self, lemma: str, search_lang="EN", **kwargs):
        return self.session.get(
            f"{BABELNET_BASE_URL}/getSynsetIds",
            params={"lemma": lemma, "searchLang": search_lang, **kwargs, },
        ).json()

    def get_babel_sense_data(self, synset_id, search_lang="IT",**kwargs):
        return self.session.get(
            f"{BABELNET_BASE_URL}/getSynset",
            params={'id': synset_id, "targetLang": search_lang, **kwargs, },
        ).json()


def babel_missing():
    syn_map = get_synset_map()
    id_to_vector = nasari_small.nasari_small_id_to_vector()
    pairs, v1, v2 = get_pairs_values()
    b1_missing = [b for p in pairs for b in syn_map[p[0]] if b not in id_to_vector]
    b2_missing = [b for p in pairs for b in syn_map[p[1]] if b not in id_to_vector]
    return b1_missing + b2_missing


def get_dict_from_json(file_path="resources/missing.json"):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def get_lemmas_from_sense(senses: Dict):
    if "message" not in senses.keys():
        lemmas = [sense["properties"]['simpleLemma'] for sense in senses["senses"]]


def retrieve_lemmas_from_babel_missing():
    result = {}
    for id in babel_missing():
        client = BabelNetClient('cddb74a9-cc73-410e-a386-8127531dc104')
        json = client.get_babel_sense_data(id)
        lemmas = get_lemmas_from_sense(json)
        result[id] = lemmas
        save_dict(result, "missing.json")


# def retrieve_example():
#     result = {}
#     ids = ['bn:00023796n', 'bn:21169671n']
#     for id in ids:
#         client = BabelNetClient('cddb74a9-cc73-410e-a386-8127531dc104')
#         json = client.get_babel_sense_data(id)
#         lemmas = get_lemmas_from_sense(json)
#         result[id] = lemmas
#     save_dict(result)


# def get_single_sinset(id):
#     client = BabelNetClient('cddb74a9-cc73-410e-a386-8127531dc104')
#     json = client.get_babel_sense_data(id)
#     return json