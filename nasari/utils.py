from nasari_parser import build_lemma_index, read_nasari_resource
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_lemmas_from_source():
    f = open("resources/dd-small-nasari-15.txt", "r")
    lines = f.read().splitlines()
    vectors = read_nasari_resource(lines)
    return build_lemma_index(vectors)


def get_filtered_words(text):
    return [word for word in word_tokenize(text) if not_stop_or_punct(word)]


def disambiguation(vector, text_path):
    text = open(text_path, "r").read()
    text_words = get_filtered_words(text)
    return max([v for v in vector], key=lambda v: set(v.weights) & set(text_words))


def get_context(topic, text_path):
    nasari = get_lemmas_from_source()
    return {w: disambiguation(nasari.get(w), text_path) for vector in topic.values() for w in vector.weights.keys()}


def not_stop_or_punct(word):
    stop_words = set(stopwords.words('english'))
    return not word.lower() in stop_words and word.isalnum()


def get_filtered_title(text_path):
    f = open(text_path, "r")
    title = f.readline()
    return [word for word in get_filtered_words(title)]


def get_dis_vectors(text, text_path):
    nasari = get_lemmas_from_source()
    return {word: disambiguation(nasari[word], text_path) for word in text if word in nasari}


def get_dis_topic_from_text(text_path):
    title = get_filtered_title(text_path)
    topic = get_dis_vectors(title, text_path)
    return {word: vector for word, vector in topic.items()}


