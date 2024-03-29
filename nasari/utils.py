import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def not_stop_or_punct(word):
    stop_words = set(stopwords.words("english"))
    return word.lower() not in stop_words and word.isalnum()


def get_filtered_words(text):
    return [word for word in word_tokenize(text) if not_stop_or_punct(word)]


def disambiguation(vector, text):
    return max(vector, key=lambda v: set(v) & set(text))


def get_context(topic, text, nasari):
    return {
        w: disambiguation(nasari.get(w), text)
        for vector in topic.values()
        for w in vector.keys()
    }


def get_filtered_title(text_path):
    with open(text_path, "r") as f:
        title = f.readline()
        return [word for word in get_filtered_words(title)]


def get_dis_vectors(text, nasari):
    return {
        word: disambiguation(nasari[word], text)
        for word in text
        if word in nasari
    }


def get_dis_topic_from_text(text, nasari):
    topic = get_dis_vectors(text, nasari)
    return {word: vector for word, vector in topic.items()}


def write(title, text, comp, type):
    name = os.path.join("output", f"{title}{comp!s}{type}.txt")
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, "w") as f:
        f.write(text)


def get_words(text_path):
    with open(text_path, "r") as f:
        text = f.read()
        return [
            word for word in word_tokenize(text) if not_stop_or_punct(word)
        ]
