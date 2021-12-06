from nasari_parser import build_lemma_index, read_nasari_resource
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_lemmas_from_source():
    f = open("resources/dd-small-nasari-15.txt", "r")
    lines = f.read().splitlines()
    vectors = read_nasari_resource(lines)
    return build_lemma_index(vectors)


def not_stop_or_punct(word):
    stop_words = set(stopwords.words('english'))
    return not word.lower() in stop_words and word.isalnum()


def get_filtered_words(text):
    return [word for word in word_tokenize(text) if not_stop_or_punct(word)]


def disambiguation(vector, text):
    return max([v for v in vector], key=lambda v: set(v.weights) & set(text))


def get_context(topic, text, nasari):
    return {w: disambiguation(nasari.get(w), text) for vector in topic.values() for w in vector.weights.keys()}


def get_filtered_title(text_path):
    f = open(text_path, "r")
    title = f.readline()
    return [word for word in get_filtered_words(title)]


def get_dis_vectors(text, nasari):
    return {word: disambiguation(nasari[word], text) for word in text if word in nasari}


def get_dis_topic_from_text(text, nasari):
    title = get_filtered_title(text)
    topic = get_dis_vectors(text, nasari)
    return {word: vector for word, vector in topic.items()}


def write(title, text, comp):
    name = "output//" + title + str(comp) + ".txt"
    f = open(name, "w")
    f.write(text)
    f.close()


def get_words(text_path):
    text = open(text_path, "r").read()
    return [word for word in word_tokenize(text) if not_stop_or_punct(word)]