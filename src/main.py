from typing import List, Callable

from src.models import korean, grammar
from src.type import ModelDescription
from src.util import generate, preview, extract_data


def vocab_model() -> ModelDescription:
    csv_path = "../data/tsv/korean2a.tsv"
    deck_title = "Korean Vocab 2A"
    columns = [1, 2, 3]
    model = korean.create_model()
    return csv_path, deck_title, columns, model


def grammar_model() -> ModelDescription:
    csv_path = "../data/tsv/grammar2a.tsv"
    deck_title = "Korean Grammar 2A"
    columns = [1, 2, 3]
    model = grammar.create_model()
    return csv_path, deck_title, columns, model


def generate_and_preview(model_func: Callable[[], ModelDescription], show_preview: bool = False, vocab_range: List[int] = [0, -1]):
    csv_path, deck_title, columns, model = model_func()
    print(f'[ Generating {deck_title} ]')

    print(' ├ Extracting Data')
    data = extract_data(csv_path, columns, model)
    print(' ├ Generating Anki Deck')
    generate(data, csv_path, deck_title, model)
    print(' └ DONE')

    if show_preview:
        # slice data if necessary
        vocab_range[1] = len(data) if vocab_range[1] == -1 else vocab_range[1]
        data = data[vocab_range[0]:vocab_range[1]]

        preview(data, model)


if __name__ == '__main__':
    generate_and_preview(vocab_model)
    generate_and_preview(grammar_model, show_preview=True, vocab_range=[-1,-1])
