from pathlib import Path

from nltk.corpus import framenet

from framenet.bow_mapper import bow_mapper
from framenet.frame_mapping import yaml
from framenet.map_frame import map_frame
from framenet.subgraph_mapper import subgraph_mapper

ANNOTATED_PATH = Path(__file__).parent / 'resources' / 'annotations.yaml'


def mappings_accuracy(mappings):
    with ANNOTATED_PATH.open() as annotated_file:
        annotated = yaml.load(annotated_file)

    wrong = 0
    total = 0

    for golden_frame_mapping, test_frame_mapping in zip(annotated, mappings):
        assert golden_frame_mapping.frame.ID == test_frame_mapping.frame.ID

        for g, t in zip(golden_frame_mapping.mappings(), test_frame_mapping.mappings()):
            differences = sorted(set(g.items()) ^ set(t.items()))
            wrong += len(differences) / 2
            total += len(g)

    return 1 - wrong/total


ids_caputo = [1594, 422, 1812, 2140, 118]
ids_gentiletti = [308, 1943, 2430, 333, 381]


def main():
    frames = [framenet.frame(i) for i in ids_caputo + ids_gentiletti]

    bow_frames = [map_frame(frame, bow_mapper) for frame in frames]
    subgraph_frames = [map_frame(frame, subgraph_mapper) for frame in frames]

    for mapped_frame in bow_frames:
        print(mapped_frame)

    print(f"Accuracy (BOW):      {mappings_accuracy(bow_frames):.2%}")
    print(f"Accuracy (subgraph): {mappings_accuracy(subgraph_frames):.2%}")


if __name__ == '__main__':
    main()
