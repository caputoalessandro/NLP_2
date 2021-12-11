from dataclasses import dataclass
from typing import Any, ClassVar

from nltk.corpus import framenet, wordnet as wn
from nltk.corpus.reader import Synset, AttrDict
from tabulate import tabulate

from ruamel.yaml import YAML, yaml_object

yaml = YAML()


def _tabulate_pairing(pairing: dict[str, Synset]):
    return tabulate([(name, synset.name()) for name, synset in pairing.items()], tablefmt='fancy_grid')


@yaml_object(yaml)
@dataclass
class FrameMapping:
    frame: Any
    name: dict[str, Synset]
    frame_elements: dict[str, Synset]
    lexical_units: dict[str, Synset]

    def mappings(self):
        return self.name, self.frame_elements, self.lexical_units

    def __str__(self):
        return f"""
------------------------------------------------------------
Mapping for frame "{self.frame.name}". {len(self.frame_elements)} FEs and {len(self.lexical_units)} LUs.

{_tabulate_pairing(self.name)}

# Frame Elements

{_tabulate_pairing(self.frame_elements)}

# Lexical Units

{_tabulate_pairing(self.lexical_units)}
"""


def synset_constructor(loader, node):
    return wn.synset(loader.construct_scalar(node))


def synset_representer(dumper, synset: Synset):
    return dumper.represent_scalar('!wn', synset.name())


yaml.constructor.add_constructor('!wn', synset_constructor)
yaml.representer.add_representer(Synset, synset_representer)


def frame_constructor(loader, node):
    return framenet.frame(int(loader.construct_scalar(node)))


def frame_representer(dumper, frame: AttrDict):
    return dumper.represent_scalar('!fn', str(frame.ID))


yaml.constructor.add_constructor('!fn', frame_constructor)
yaml.representer.add_representer(AttrDict, frame_representer)

yaml.representer.ignore_aliases = lambda *_: True
