from utils import get_context, get_dis_topic_from_text, get_words
from nasari.nasari_small import nasari_small_lemma_to_vector
from paragraph import ordered_paragraph_by_score, compress, write_ranked_paragraphs
from evaluation import rouge, bleu
from pathlib import Path


def print_accuracies(type, compression, paragraphs, text):
    print("---------------------------------------------")
    print("ranked by ", type, str(compression) + "%")
    print("recall: ", rouge(paragraphs, text))
    print("precision: ", bleu(paragraphs, text))


def summarization(text_path):
    nasari = nasari_small_lemma_to_vector()
    text = get_words(text_path)
    topic = get_dis_topic_from_text(text_path, nasari)
    context = get_context(topic, text, nasari)
    ordered = ordered_paragraph_by_score(text_path, context, nasari)

    print("---------------------------------------------")
    print(">>>>>>>>>> ", text_path, " <<<<<<<<<<")
    for compression in range(10, 31, 10):
        compressed = compress(ordered, compression)
        by_title, by_cohesion = write_ranked_paragraphs(compressed, text_path, compression)
        print_accuracies("title", compression, by_title, text)
        print_accuracies("cohesion", compression, by_cohesion, text)


if __name__ == "__main__":
    p = Path('text')
    for x in p.iterdir():
        summarization(str(x))
