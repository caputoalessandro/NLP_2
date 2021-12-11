from pathlib import Path
from framenet.bow_mapping import bow_mapping
from framenet.frame_mapping import yaml

ANNOTATED_PATH = Path(__file__).parent / 'resources' / 'annotations.yaml'


def main():
    with ANNOTATED_PATH.open() as annotated_file:
        annotated = yaml.load(annotated_file)

    mappings = bow_mapping()

    wrong = 0
    total = 0

    for golden_frame_mapping, test_frame_mapping in zip(annotated, mappings):
        assert golden_frame_mapping.frame.ID == test_frame_mapping.frame.ID

        for g, t in zip(golden_frame_mapping.mappings(), test_frame_mapping.mappings()):
            differences = sorted(set(g.items()) ^ set(t.items()))
            wrong += len(differences) / 2
            total += len(g)

    print(f"Accuracy: {wrong/total:.2%}")


if __name__ == '__main__':
    main()
