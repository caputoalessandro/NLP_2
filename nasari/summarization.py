from nasari_parser import build_lemma_index, read_nasari_resource
from nltk.wsd import lesk


def get_topic(text, lemmas):
    lines_to_read = len(text)//15
    words = [word for line in text[:lines_to_read] for word in line.split()]
    return {word: lemmas[word] for word in words if word in lemmas}


def disambiguation(vector):
    return 0


def topic_disambiguation(topic):
    return {word: (disambiguation(vector) if len(vector) > 1 else vector) for word, vector in topic.items()}


def weighted_overlap(v1, v2):
    return 0


def get_paragraphs():
    pass


def get_lemmas_from_source():
    f = open("resources/dd-small-nasari-15.txt", "r")
    lines = f.read().splitlines()
    vectors = read_nasari_resource(lines)
    return build_lemma_index(vectors)


def get_text(path):
    f = open(path, "r")
    text = f.read().splitlines()
    return [line for line in text if line]


def summarization():
    text_path = "resources/Trump-wall.txt"
    text = get_text(text_path)
    lemmas = get_lemmas_from_source()
    topic = get_topic(text, lemmas)
    topic = topic_disambiguation(topic)

    return 0


if __name__ == "__main__":
    summarization()