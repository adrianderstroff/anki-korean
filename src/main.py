from src.models import korean, grammar
from src.util import generate, preview, extract_data


def vocab_model():
    csv_path = "../data/tsv/korean2a.csv"
    deck_title = "Korean Vocab 2A"
    columns = [1, 2, 3]
    model = korean.create_model()
    return csv_path, deck_title, columns, model


def grammar_model():
    csv_path = "../data/tsv/grammar2a.tsv"
    deck_title = "Korean Grammar 2A"
    columns = [1, 2, 3]
    model = grammar.create_model()
    return csv_path, deck_title, columns, model


def generate_and_preview(model_func):
    csv_path, deck_title, columns, model = model_func()

    data = extract_data(csv_path, columns, model)
    generate(data, csv_path, deck_title, model)
    preview(data, model)


if __name__ == '__main__':
    # generate_and_preview(vocab_model)
    generate_and_preview(grammar_model)
