from utils import get_context, get_dis_topic_from_text, get_words
from nasari.nasari_parser import nasari_lemma_to_vectors
from paragraph import get_salient_paragraphs
from evaluation import rouge, bleu


def summarization(text_path, type, compression):
    nasari = nasari_lemma_to_vectors()
    text = get_words(text_path)
    topic = get_dis_topic_from_text(text_path, nasari)
    context = get_context(topic, text, nasari)
    summmary = get_salient_paragraphs(text_path, context, compression, type, nasari, type)
    print("---------------------------------------------")
    print(type, str(compression) + "%")
    print("recall: ", rouge(summmary, text))
    print("precision: ", bleu(summmary, text))
    return 0


if __name__ == "__main__":
    summarization("resources/Andy-Warhol.txt", "cohesion", 10)
    summarization("resources/Andy-Warhol.txt", "cohesion", 20)
    summarization("resources/Andy-Warhol.txt", "cohesion", 30)
    summarization("resources/Andy-Warhol.txt", "title", 10)
    summarization("resources/Andy-Warhol.txt", "title", 20)
    summarization("resources/Andy-Warhol.txt", "title", 30)