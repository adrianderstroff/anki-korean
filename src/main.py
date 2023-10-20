from typing import List, Callable

from src.logger import Logger
from src.models import korean, grammar, travelvocab
from src.type import ModelDescription
from src.util import generate, preview, extract_data


Logger.set_log_file('../data/log.json')


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


def travel_vocab_model() -> ModelDescription:
    csv_path = "../data/tsv/travelvocab.tsv"
    deck_title = "Korean Travel Vocab"
    columns = [1, 2]
    model = travelvocab.create_model()
    return csv_path, deck_title, columns, model


def generate_and_preview(model_func: Callable[[], ModelDescription], show_preview: bool = False, vocab_range: List[int] = [0, -1]):
    csv_path, deck_title, columns, model = model_func()
    Logger.print(f'[ Generating {deck_title} ]')

    Logger.print(' ├ Extracting Data')
    data = extract_data(csv_path, columns, model)
    Logger.print(' ├ Generating Anki Deck')
    generate(data, csv_path, deck_title, model)
    Logger.print(' └ DONE')

    if show_preview:
        # slice data if necessary
        vocab_range[1] = len(data) if vocab_range[1] == -1 else vocab_range[1]
        data = data[vocab_range[0]:vocab_range[1]]

        preview(data, model)


if __name__ == '__main__':
    generate_and_preview(vocab_model)
    generate_and_preview(grammar_model)
    # generate_and_preview(travel_vocab_model, show_preview=True)
