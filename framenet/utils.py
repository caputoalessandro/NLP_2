import nltk
from nltk.corpus import framenet as fn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def get_frame_from_id_list(ids):
    return [fn.frame(id) for id in ids]


def get_noun(tagged):
    for w, t in reversed(tagged):
        if t == "NOUN":
            return w


def get_verb(tagged):
    for w, t in reversed(tagged):
        if t == "VERB":
            return w


def get_adp_noun(tagged):
    adp = False
    for w, t in reversed(tagged):
        if t == "ADP":
            adp = True
            continue
        if adp and t == "NOUN":
            return w


def get_regent(multiword):
    if not isinstance(multiword, list):
        multiword = multiword.split("_")

    tagged = nltk.pos_tag(multiword, "universal")
    tags = [t[1] for t in tagged]

    if "ADP" in tags:
        return get_adp_noun(tagged)
    elif "VERB" in tags and "NOUN" in tags:
        return get_verb(tagged)
    else:
        return get_noun(tagged)


def is_multiword(word):
    if '_' in word:
        splitted = word.split("_")
    else:
        splitted = word.split()

    return len(splitted) > 1


def preprocessing(sentence):
    lemmatizer = WordNetLemmatizer()
    stopWords = set(stopwords.words('english'))
    return [lemmatizer.lemmatize(word) for word in sentence.split() if word.isalnum() and word not in stopWords]