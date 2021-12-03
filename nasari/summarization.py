from utils import get_context, get_dis_topic_from_text
from paragraph import get_salient_paragraphs


def summarization(text_path):
    topic = get_dis_topic_from_text(text_path)
    context = get_context(topic, text_path)
    summ = get_salient_paragraphs(text_path, context, 30, "cohesion")
    print(p for p in summ)
    return 0


if __name__ == "__main__":
    summarization("resources/Andy-Warhol.txt")
