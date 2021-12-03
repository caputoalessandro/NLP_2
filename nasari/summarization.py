from utils import get_context, get_dis_topic_from_text, get_lemmas_from_source
from paragraph import get_salient_paragraphs


def summarization(text_path):
    nasari = get_lemmas_from_source()
    topic = get_dis_topic_from_text(text_path, nasari)
    context = get_context(topic, text_path, nasari)
    summ = get_salient_paragraphs(text_path, context, 30, "cohesion", nasari)
    print(summ)
    return 0


if __name__ == "__main__":
    summarization("resources/Andy-Warhol.txt")
