from utils import get_context, get_dis_topic_from_text, get_lemmas_from_source, write
from paragraph import get_salient_paragraphs
from evaluation import rouge, bleu


def summarization(text_path):
    nasari = get_lemmas_from_source()
    topic = get_dis_topic_from_text(text_path, nasari)
    context = get_context(topic, text_path, nasari)
    summmary = get_salient_paragraphs(text_path, context, 10, "cohesion", nasari)
    print("recall: ", rouge(summmary, text_path))
    print("precision: ", bleu(summmary, text_path))
    return 0


if __name__ == "__main__":
    # for filename in os.listdir("resources"):
    #     summarization("resources/" + filename)
    summarization("resources/Andy-Warhol.txt")
