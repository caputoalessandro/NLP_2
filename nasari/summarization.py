from utils import get_context, get_dis_topic_from_text, get_lemmas_from_source, write
from paragraph import get_salient_paragraphs
from evaluation import rouge, bleu
from utils import get_words


def summarization(text_path):
    nasari = get_lemmas_from_source()
    text = get_words(text_path)
    topic = get_dis_topic_from_text(text_path, nasari)
    context = get_context(topic, text, nasari)
    summmary = get_salient_paragraphs(text_path, context, 10, "cohesion", nasari)
    print("recall: ", rouge(summmary, text))
    print("precision: ", bleu(summmary, text))
    return 0


if __name__ == "__main__":
    # for filename in os.listdir("resources"):
    #     summarization("resources/" + filename)
    summarization("resources/Andy-Warhol.txt")
